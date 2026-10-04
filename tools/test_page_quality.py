"""Guard local typography, accessible image markup and the initial loading path."""
from html.parser import HTMLParser
from pathlib import Path
import json
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


class Tags(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []

    def handle_starttag(self, tag, attributes):
        self.tags.append((tag, dict(attributes)))


class PageQuality(unittest.TestCase):
    def test_shared_theme_loads_before_styles_and_defines_component_variables(self):
        theme = ROOT / 'assets/css/theme.css'
        defined = set(re.findall(r'(--niche-[\w-]+)\s*:', theme.read_text()))
        for page in ROOT.rglob('*.html'):
            parser = Tags()
            parser.feed(page.read_text())
            styles = [(page.parent / attrs['href']).resolve() for tag, attrs in parser.tags
                      if tag == 'link' and attrs.get('rel') == 'stylesheet']
            self.assertEqual(styles.count(theme), 1, str(page))
            self.assertLess(styles.index(theme), styles.index(ROOT / 'assets/css/style.css'), str(page))
        for path in [*ROOT.rglob('*.html'), *ROOT.glob('assets/css/*.css'),
                     ROOT / 'assets/plugins/hmenu/ace-responsive-menu.css',
                     ROOT / 'assets/plugins/horizontaltimeline/timeline-style.css']:
            referenced = set(re.findall(r'var\((--niche-[\w-]+)', path.read_text()))
            self.assertFalse(referenced - defined, f'{path}: undefined theme variables {referenced - defined}')

    def test_every_page_has_a_skip_target_zoom_and_local_fonts(self):
        for page in ROOT.rglob('*.html'):
            parser = Tags()
            parser.feed(page.read_text())
            tags = parser.tags
            ids = [attrs['id'] for _, attrs in tags if 'id' in attrs]
            self.assertEqual(len(ids), len(set(ids)), str(page))
            self.assertEqual(sum(attrs.get('id') == 'main-content' for _, attrs in tags), 1, str(page))
            self.assertTrue(any(tag == 'a' and attrs.get('href') == '#main-content' for tag, attrs in tags), str(page))
            viewport = next(attrs['content'] for tag, attrs in tags if tag == 'meta' and attrs.get('name') == 'viewport')
            self.assertNotIn('maximum-scale', viewport, str(page))
            self.assertNotIn('user-scalable', viewport, str(page))
            links = [attrs.get('href', '') for tag, attrs in tags if tag == 'link']
            self.assertTrue(any('poppins-5.3.0/poppins.css' in link for link in links), str(page))
            self.assertFalse(any('fonts.googleapis' in link for link in links), str(page))

    def test_images_reserve_space_and_logos_load_immediately(self):
        lazy = 0
        for page in ROOT.rglob('*.html'):
            parser = Tags()
            parser.feed(page.read_text())
            for tag, attrs in parser.tags:
                if tag != 'img':
                    continue
                self.assertIn('alt', attrs, str(page))
                if not attrs.get('src'):
                    continue  # The lightbox sets its image when it opens.
                self.assertGreater(int(attrs['width']), 0, str(page))
                self.assertGreater(int(attrs['height']), 0, str(page))
                self.assertIn(attrs.get('loading'), ('lazy', 'eager'), str(page))
                lazy += attrs.get('loading') == 'lazy'
                if 'logo' in attrs['src']:
                    self.assertEqual(attrs['loading'], 'eager', str(page))
        self.assertGreater(lazy, 0)

    def test_optimized_images_and_font_binaries_are_local(self):
        manifest = json.loads((ROOT / 'tools/image_optimization.json').read_text())
        for source, asset in manifest.items():
            self.assertTrue((ROOT / source).is_file())
            data = (ROOT / asset['target']).read_bytes()
            self.assertTrue(data.startswith(b'RIFF') and data[8:12] == b'WEBP')
            self.assertLess(len(data), (ROOT / source).stat().st_size * .9)
        folder = ROOT / 'assets/plugins/poppins-5.3.0'
        css = (folder / 'poppins.css').read_text()
        self.assertEqual(set(re.findall(r'font-weight:\s*(\d+)', css)), {'300', '400', '500', '600', '700'})
        fonts = re.findall(r'url\(\./([^)]*)\)', css)
        self.assertEqual(len(fonts), 15)
        for font in fonts:
            self.assertTrue((folder / font).read_bytes().startswith(b'wOF2'))
        self.assertIn('SIL OPEN FONT LICENSE', (folder / 'LICENSE').read_text())


if __name__ == '__main__':
    unittest.main()
