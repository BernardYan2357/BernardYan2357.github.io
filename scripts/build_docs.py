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
WIKILINK = re.compile(r'(?<!!)(?<!\[)!?\[\[([^\[\]\n]+)\]\](?!\()')
FENCE = re.compile(r'^\s*(`{3,}|~{3,})')
LIST = re.compile(r'^( *)(?:[-+*]|\d+[.)])\s+')


class Images:
    kind = 'image'

    def __init__(self, docs: Path):
        self.docs = docs.resolve()
        self.files = sorted(p for p in self.docs.rglob('*') if p.suffix.lower() in IMAGE_SUFFIXES)
        self.count = 0

    def resolve(self, target: str, note: Path) -> Path:
        for path in (note.parent / target, self.docs / target):
            path = path.resolve()
            if not path.is_relative_to(self.docs):
                continue
            # Return the indexed spelling, rather than trusting Windows' case-insensitive lookup.
            exact = [p for p in self.files if p == path and str(p) == str(path)]
            if exact:
                return exact[0]
            matches = [p for p in self.files if str(p).casefold() == str(path).casefold()]
            if len(matches) == 1:
                return matches[0]
            if len(matches) > 1:
                raise ValueError(f'{note.relative_to(self.docs)}: ambiguous {self.kind}: {target}: {matches}')
        candidates = [p for p in self.files if p.relative_to(self.docs).as_posix() == target
                      or p.relative_to(self.docs).as_posix().endswith('/' + target)]
        if not candidates:
            candidates = [p for p in self.files
                          if p.relative_to(self.docs).as_posix().casefold() == target.casefold()
                          or p.relative_to(self.docs).as_posix().casefold().endswith('/' + target.casefold())]
        if not candidates:
            raise ValueError(f'{note.relative_to(self.docs)}: {self.kind} not found: {target}')
        # Prefer the nearest folder, but never silently choose between equal matches.
        def distance(path: Path) -> int:
            common = Path(os.path.commonpath([note.parent, path.parent]))
            return len(note.parent.relative_to(common).parts) + len(path.parent.relative_to(common).parts)
        nearest = min(map(distance, candidates))
        candidates = [p for p in candidates if distance(p) == nearest]
        if len(candidates) != 1:
            raise ValueError(f'{note.relative_to(self.docs)}: ambiguous {self.kind}: {target}: {candidates}')
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


class Links(Images):
    kind = 'note'

    def __init__(self, docs: Path):
        self.docs = docs.resolve()
        self.files = sorted(p for p in self.docs.rglob('*') if p.is_file())
        self.count = 0
        self.unresolved: set[str] = set()

    def replace(self, match: re.Match[str], note: Path) -> str:
        from pymdownx.slugs import slugify

        reference, _, alias = match[1].replace(r'\|', '|').partition('|')
        target, separator, heading = unquote(reference.strip()).partition('#')
        target = target.strip().replace('\\', '/')
        if heading.startswith('^'):
            self.unresolved.add(f'{note.relative_to(self.docs)}: block link not supported: {reference}')
            return match[0]
        try:
            if not target:
                page = note
            elif target.endswith('.md'):
                page = self.resolve(target, note)
            else:
                try:
                    page = self.resolve(target + '.md', note)
                except ValueError as error:
                    if 'not found' not in str(error) or not Path(target).suffix:
                        raise
                    page = self.resolve(target, note)
        except ValueError as error:
            self.unresolved.add(str(error))
            return match[0]
        url = quote(Path(os.path.relpath(page, note.parent)).as_posix(), safe='/') if target else ''
        if separator:
            # Match the Unicode, lower-case TOC slugger configured in mkdocs.yml.
            url += '#' + quote(slugify(case='lower')(heading.split('#')[-1].strip(), '-'), safe='')
        label = alias.strip() or (Path(target).stem if target else '')
        if not alias and heading:
            label += (' > ' if label else '') + heading
        label = label.replace('\\', '\\\\').replace('[', r'\[').replace(']', r'\]').replace('|', '&#124;')
        self.count += 1
        return f'[{label}]({url})'

    def convert_line(self, line: str, note: Path) -> str:
        parts = re.split(r'(`+.*?`+)', line)
        return ''.join(part if i % 2 else WIKILINK.sub(lambda m: self.replace(m, note), part)
                       for i, part in enumerate(parts))


def normalize(text: str, note: Path, images: Images, links: Links | None = None) -> str:
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
        line = images.convert_line(line, note)
        result.append(links.convert_line(line, note) if links else line)
    return '\n'.join(result) + ('\n' if text.endswith('\n') else '')


def prepare(source: Path, destination: Path) -> tuple[int, int, Links]:
    shutil.copytree(source, destination)
    # Git records this directory as `linux`; Windows may retain the local spelling `Linux`.
    # Normalize only the disposable copy so local and Linux CI builds publish identical URLs.
    for folder in destination.iterdir():
        if folder.is_dir() and folder.name == 'Linux':
            temporary = destination / '.linux-case-normalization'
            if temporary.exists() or any(p.name == 'linux' for p in destination.iterdir()):
                raise ValueError('Conflicting Linux/linux directories in build input')
            folder.rename(temporary)
            temporary.rename(destination / 'linux')
    images = Images(destination)
    links = Links(destination)
    changed = 0
    for note in destination.rglob('*.md'):
        original = note.read_text(encoding='utf-8')
        converted = normalize(original, note, images, links)
        if converted != original:
            changed += 1
        note.write_text(converted, encoding='utf-8')
    return changed, images.count, links


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
        changed, images, links = prepare(project / 'docs', staging / 'docs')
        for warning in sorted(links.unresolved):
            print(f'Warning: {warning}', file=sys.stderr)
        if args.strict and links.unresolved:
            return 1
        config = (project / 'mkdocs.yml').read_text(encoding='utf-8')
        # Keep the original YAML tags intact; only the generated configuration changes paths.
        import json
        for key, path in {'docs_dir': 'docs', 'site_dir': 'site', 'cache_dir': '.cache'}.items():
            config += f'\n{key}: {json.dumps(path)}\n'
        print(f'Prepared {changed} notes; converted {images} image embeds and {links.count} wikilinks. '
              'Source notes unchanged.', flush=True)
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
