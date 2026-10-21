from pathlib import Path
import tempfile
import unittest

import markdown

from build_docs import Images, normalize, prepare


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
        changed, images = prepare(self.docs, staging)
        self.assertEqual((changed, images), (1, 1))
        self.assertEqual(self.note.read_bytes(), raw)
        text = (staging / 'vision' / 'hand.md').read_text(encoding='utf-8')
        self.assertEqual(normalize(text, self.note, self.images), text)


if __name__ == '__main__':
    unittest.main()
