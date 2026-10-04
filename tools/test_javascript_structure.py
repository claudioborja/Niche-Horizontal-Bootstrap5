"""Keep application logic external and component loading explicit."""
from project_files import html_pages
from html.parser import HTMLParser
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class Scripts(HTMLParser):
    def __init__(self):
        super().__init__()
        self.sources = []
        self.inline = []
        self.handlers = []
        self.current = None

    def handle_starttag(self, tag, attributes):
        attributes = dict(attributes)
        self.handlers.extend(key for key in attributes if key.startswith('on'))
        if tag == 'script':
            if attributes.get('src'):
                self.sources.append(attributes['src'])
            else:
                self.current = ''

    def handle_data(self, text):
        if self.current is not None:
            self.current += text

    def handle_endtag(self, tag):
        if tag == 'script' and self.current is not None:
            if self.current.strip():
                self.inline.append(self.current)
            self.current = None


class JavaScriptStructure(unittest.TestCase):
    def test_application_logic_stays_in_external_files(self):
        for page in html_pages(ROOT):
            parser = Scripts()
            parser.feed(page.read_text())
            self.assertEqual(parser.inline, [], str(page))
            self.assertEqual(parser.handlers, [], str(page))

    def test_component_modules_load_once_after_the_registry(self):
        for page in html_pages(ROOT):
            parser = Scripts()
            parser.feed(page.read_text())
            names = [source.split('assets/js/')[-1] for source in parser.sources]
            if 'niche.js' not in names:
                continue
            core = names.index('niche.js')
            for offset, module in enumerate(('layout', 'navigation', 'widgets'), start=1):
                name = 'niche/' + module + '.js'
                self.assertEqual(names.count(name), 1, str(page))
                self.assertEqual(names[core + offset], name, str(page))
            jquery = any('jquery-4.0.0/jquery.min.js' in source for source in parser.sources)
            self.assertEqual(names.count('niche/jquery-bridge.js'), int(jquery), str(page))
            if jquery:
                self.assertEqual(names[core + 4], 'niche/jquery-bridge.js', str(page))
            self.assertFalse(any('ace-responsive-menu.js' in source or 'jquery-slimscroll' in source for source in parser.sources), str(page))


if __name__ == '__main__':
    unittest.main()
