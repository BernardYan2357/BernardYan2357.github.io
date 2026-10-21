"""Build Zensical from a temporary, normalized copy of the Obsidian notes."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from urllib.parse import quote, unquote


ROOT = Path(__file__).resolve().parents[1]
IMAGE_SUFFIXES = {'.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp', '.bmp', '.avif', '.ico'}
EMBED = re.compile(r'!\[\[([^\]\n]+)\]\]')
FENCE = re.compile(r'^\s*(`{3,}|~{3,})')
LIST = re.compile(r'^( *)(?:[-+*]|\d+[.)])\s+')


class Images:
    def __init__(self, docs: Path):
        self.docs = docs.resolve()
        self.files = sorted(p for p in self.docs.rglob('*') if p.suffix.lower() in IMAGE_SUFFIXES)
        self.count = 0

    def resolve(self, target: str, note: Path) -> Path:
        for path in (note.parent / target, self.docs / target):
            path = path.resolve()
            if path.is_relative_to(self.docs) and path.is_file():
                return path
        candidates = [p for p in self.files if p.relative_to(self.docs).as_posix() == target
                      or p.relative_to(self.docs).as_posix().endswith('/' + target)]
        if not candidates:
            raise ValueError(f'{note.relative_to(self.docs)}: image not found: {target}')
        # Prefer the nearest folder, but never silently choose between equal matches.
        def distance(path: Path) -> int:
            common = Path(os.path.commonpath([note.parent, path.parent]))
            return len(note.parent.relative_to(common).parts) + len(path.parent.relative_to(common).parts)
        nearest = min(map(distance, candidates))
        candidates = [p for p in candidates if distance(p) == nearest]
        if len(candidates) != 1:
            raise ValueError(f'{note.relative_to(self.docs)}: ambiguous image: {target}: {candidates}')
        return candidates[0]

    def replace(self, match: re.Match[str], note: Path) -> str:
        target, _, option = match.group(1).partition('|')
        target = unquote(target.strip()).replace('\\', '/')
        if Path(target).suffix.lower() not in IMAGE_SUFFIXES:
            return match.group(0)  # Note and Canvas transclusion require separate handling.
        image = self.resolve(target, note)
        url = quote(Path(os.path.relpath(image, note.parent)).as_posix(), safe='/')
        dimensions = re.fullmatch(r'(\d+)(?:x(\d+))?', option.strip())
        label = image.stem if not option or dimensions else option.strip()
        label = label.replace('\\', '\\\\').replace('[', r'\[').replace(']', r'\]')
        result = f'![{label}]({url})'
        if dimensions:
            result += f'{{ width="{dimensions[1]}"'
            if dimensions[2]:
                result += f' height="{dimensions[2]}"'
            result += ' }'
        self.count += 1
        return result

    def convert_line(self, line: str, note: Path) -> str:
        # Backtick-delimited examples are content, not attachment references.
        parts = re.split(r'(`+.*?`+)', line)
        return ''.join(part if i % 2 else EMBED.sub(lambda m: self.replace(m, note), part)
                       for i, part in enumerate(parts))


def normalize(text: str, note: Path, images: Images) -> str:
    lines = text.splitlines()
    result: list[str] = []
    fence = None
    math = False
    frontmatter = bool(lines and lines[0].lstrip('\ufeff') == '---')
    in_list = False

    def blank() -> None:
        if result and result[-1].strip():
            result.append('')

    for number, line in enumerate(lines):
        stripped = line.strip()
        if frontmatter:
            result.append(line)
            if number > 0 and stripped in {'---', '...'}:
                frontmatter = False
            continue
        if fence:
            result.append(line)
            if re.fullmatch(r'\s*' + re.escape(fence[0]) + '{' + str(len(fence)) + r',}\s*', line):
                fence = None
            continue
        if math:
            result.append(line)
            if stripped == '$$':
                math = False
                result.append('')
            continue
        match = FENCE.match(line)
        if match:
            fence = match[1]
            result.append(line)
            continue
        if stripped == '$$' or (stripped.startswith('$$') and stripped.endswith('$$')):
            blank()
            result.append(line)
            if stripped == '$$':
                math = True
            else:
                result.append('')
            continue

        item = LIST.match(line)
        if item and not item[1]:
            if not in_list:
                blank()
            in_list = True
        elif stripped and not line[0].isspace():
            if in_list:
                blank()
            in_list = False
        result.append(images.convert_line(line, note))
    return '\n'.join(result) + ('\n' if text.endswith('\n') else '')


def prepare(source: Path, destination: Path) -> tuple[int, int]:
    shutil.copytree(source, destination)
    images = Images(source)
    changed = 0
    for note in source.rglob('*.md'):
        original = note.read_text(encoding='utf-8')
        converted = normalize(original, note, images)
        if converted != original:
            changed += 1
        (destination / note.relative_to(source)).write_text(converted, encoding='utf-8')
    return changed, images.count


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--clean', action='store_true', help='Clear the Zensical build cache')
    parser.add_argument('--strict', action='store_true', help='Fail on Zensical warnings')
    args = parser.parse_args()
    project = ROOT / 'myDocs'
    cache = project / '.cache'
    cache.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='obsidian-', dir=cache) as directory:
        staging = Path(directory)
        changed, images = prepare(project / 'docs', staging / 'docs')
        config = (project / 'mkdocs.yml').read_text(encoding='utf-8')
        # Keep the original YAML tags intact; only the generated configuration changes paths.
        import json
        for key, path in {'docs_dir': 'docs', 'site_dir': 'site', 'cache_dir': '.cache'}.items():
            config += f'\n{key}: {json.dumps(path)}\n'
        print(f'Prepared {changed} notes; converted {images} image embeds. Source notes unchanged.', flush=True)
        config_file = staging / 'mkdocs.yml'
        config_file.write_text(config, encoding='utf-8')
        command = [sys.executable, '-m', 'zensical', 'build', '-f', str(config_file)]
        command += [flag for flag, enabled in [('--clean', args.clean), ('--strict', args.strict)] if enabled]
        status = subprocess.run(command, cwd=staging, check=False).returncode
        if status:
            return status
        output = project / 'site'
        if output.is_symlink() or output.resolve() != project.resolve() / 'site':
            raise ValueError(f'Unexpected generated output directory: {output}')
        if output.exists():
            shutil.rmtree(output)
        shutil.copytree(staging / 'site', output)
        return 0


if __name__ == '__main__':
    raise SystemExit(main())
