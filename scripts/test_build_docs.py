from pathlib import Path
import tempfile
import unittest

import markdown

from build_docs import Images, Links, normalize, prepare


class PreprocessingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.docs = Path(self.temp.name) / 'docs'
        self.folder = self.docs / 'vision'
        (self.folder / 'image').mkdir(parents=True)
        self.image = self.folder / 'image' / 'eye in hand.png'
        self.image.write_bytes(b'fixture')
        self.note = self.folder / 'hand.md'
        self.images = Images(self.docs)

    def render(self, text):
        return markdown.markdown(normalize(text, self.note, self.images), extensions=[
            'attr_list', 'pymdownx.superfences', 'pymdownx.arithmatex', 'pymdownx.tasklist'
        ], extension_configs={'pymdownx.arithmatex': {'generic': True}})

    def test_image_path_and_dimensions(self):
        html = self.render('![[eye in hand.png | 500x200]]')
        self.assertIn('src="image/eye%20in%20hand.png"', html)
        self.assertIn('width="500"', html)
        self.assertIn('height="200"', html)

    def test_tight_math_and_list_render_as_separate_blocks(self):
        html = self.render('Derivation:\n$$\nx^2 + y^2 = 1\n$$\n- first\n- second\nExplanation')
        self.assertIn('<div class="arithmatex">', html)
        self.assertIn('<ul>', html)
        self.assertIn('</ul>\n<p>Explanation</p>', html)
        self.assertIn('<li>first</li>', html)

    def test_list_can_start_after_paragraph(self):
        html = self.render('Note:\n- first\n    - nested\n- second\nAfter')
        self.assertIn('<p>Note:</p>\n<ul>', html)
        self.assertIn('</ul>\n<p>After</p>', html)
        self.assertEqual(html.count('<ul>'), 2)

    def test_frontmatter_fences_inline_code_and_math_are_preserved(self):
        text = ('---\ntitle: "![[missing.png]]"\n---\n\n'
                '```markdown\n![[missing.png]]\nText\n- item\n$$\nx\n$$\n```\n\n'
                '`![[missing.png]]` and ``![[missing.png]]``\n\n'
                '$$\nx - y\n- z\n$$\n')
        self.assertEqual(normalize(text, self.note, self.images), text + '\n')
        self.assertEqual(self.images.count, 0)

    def test_note_and_canvas_embeds_are_not_images(self):
        text = '![[other note]]\n![[diagram.canvas]]\n'
        self.assertEqual(normalize(text, self.note, self.images), text)

    def test_missing_and_ambiguous_images_fail(self):
        with self.assertRaisesRegex(ValueError, 'not found'):
            normalize('![[missing.png]]', self.note, self.images)
        other = self.folder / 'attachments'
        other.mkdir()
        (other / self.image.name).write_bytes(b'duplicate')
        with self.assertRaisesRegex(ValueError, 'ambiguous'):
            normalize('![[eye in hand.png]]', self.note, Images(self.docs))

    def test_prepare_changes_only_staged_copy_and_is_idempotent(self):
        raw = b'Intro\r\n- item\r\n![[eye in hand.png]]\r\n'
        self.note.write_bytes(raw)
        staging = Path(self.temp.name) / 'staging'
        changed, images, links = prepare(self.docs, staging)
        self.assertEqual((changed, images), (1, 1))
        self.assertEqual(self.note.read_bytes(), raw)
        text = (staging / 'vision' / 'hand.md').read_text(encoding='utf-8')
        self.assertEqual(normalize(text, self.note, self.images), text)

    def test_wikilinks_with_spaces_unicode_headings_and_aliases(self):
        target = self.folder / 'PnP \u4f4d\u59ff\u4f30\u8ba1.md'
        target.write_text('# PnP\n\n## Camera 2 Base\n', encoding='utf-8')
        links = Links(self.docs)
        text = ('[[PnP \u4f4d\u59ff\u4f30\u8ba1]] [[PnP \u4f4d\u59ff\u4f30\u8ba1#Camera 2 Base|pose]] '
                '[[#\u516c\u5f0f\u63a8\u5bfc]]')
        converted = normalize(text, self.note, self.images, links)
        html = markdown.markdown(converted)
        self.assertIn('href="PnP%20%E4%BD%8D%E5%A7%BF%E4%BC%B0%E8%AE%A1.md"', html)
        self.assertIn('.md#camera-2-base">pose</a>', html)
        self.assertIn('href="#%E5%85%AC%E5%BC%8F%E6%8E%A8%E5%AF%BC"', html)
        self.assertEqual(links.count, 3)
        self.assertFalse(links.unresolved)

    def test_wikilinks_relative_paths_and_escaped_table_alias(self):
        target = self.docs / 'other' / 'page.md'
        target.parent.mkdir()
        target.write_text('# Page\n', encoding='utf-8')
        links = Links(self.docs)
        converted = normalize('[[other/page.md\\|alias]]', self.note, self.images, links)
        self.assertEqual(converted, '[alias](../other/page.md)')

    def test_wikilinks_skip_examples_and_report_missing_targets(self):
        links = Links(self.docs)
        text = ('---\ntitle: "[[missing]]"\n---\n\n'
                '```markdown\n[[missing]]\n```\n\n'
                '`[[missing]]` and ![[missing]]\n\n[[absent]]\n')
        self.assertEqual(normalize(text, self.note, self.images, links), text)
        self.assertEqual(len(links.unresolved), 2)
        self.assertTrue(any('absent' in item for item in links.unresolved))

    def test_ambiguous_wikilinks_are_reported(self):
        for folder in ['one', 'two']:
            path = self.docs / folder / 'same.md'
            path.parent.mkdir()
            path.write_text('# Same', encoding='utf-8')
        links = Links(self.docs)
        self.assertEqual(normalize('[[same]]', self.note, self.images, links), '[[same]]')
        self.assertIn('ambiguous note', next(iter(links.unresolved)))

    def test_note_and_canvas_embeds_become_links_but_images_stay_images(self):
        (self.folder / 'other.md').write_text('# Other\n\n## Details', encoding='utf-8')
        (self.folder / 'diagram.canvas').write_text('{"nodes":[],"edges":[]}', encoding='utf-8')
        links = Links(self.docs)
        text = '![[other#Details|Read more]] ![[diagram.canvas]] ![[eye in hand.png|500]]'
        converted = normalize(text, self.note, self.images, links)
        self.assertIn('[Read more](other.md#details)', converted)
        self.assertIn('[diagram](diagram.canvas)', converted)
        self.assertIn('![eye in hand](image/eye%20in%20hand.png){ width="500" }', converted)
        self.assertNotIn('![[', converted)
        self.assertEqual(links.count, 2)
        self.assertFalse(links.unresolved)

    def test_case_mismatch_uses_actual_indexed_path(self):
        folder = self.docs / 'linux'
        folder.mkdir()
        (folder / '\u56fe\u5f62.md').write_text('# Graphics', encoding='utf-8')
        links = Links(self.docs)
        text = normalize('[[Linux/\u56fe\u5f62]]', self.note, self.images, links)
        self.assertEqual(text, '[\u56fe\u5f62](../linux/%E5%9B%BE%E5%BD%A2.md)')

    def test_staging_normalizes_linux_directory_without_changing_source(self):
        folder = self.docs / 'Linux'
        folder.mkdir()
        (folder / '\u56fe\u5f62.md').write_text('# Graphics', encoding='utf-8')
        self.note.write_text('[[Linux/\u56fe\u5f62]]', encoding='utf-8')
        staging = Path(self.temp.name) / 'staging'
        prepare(self.docs, staging)
        self.assertIn('linux', [p.name for p in staging.iterdir()])
        self.assertNotIn('Linux', [p.name for p in staging.iterdir()])
        self.assertIn('Linux', [p.name for p in self.docs.iterdir()])
        self.assertIn('../linux/%E5%9B%BE%E5%BD%A2.md', (staging/'vision'/'hand.md').read_text(encoding='utf-8'))


if __name__ == '__main__':
    unittest.main()
