#!/usr/bin/env python3
"""Check HTML assets and recursively inspect locally loaded CSS resources."""
from html.parser import HTMLParser
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]


def check(root):
    pending = []
    stylesheets = set()
    missing = set()
    resources = set()

    def reference(source, value):
        if not value or value.startswith(('#', 'data:', 'blob:')):
            return
        parsed = urlsplit(value)
        if parsed.scheme or parsed.netloc:
            return
        target = (source.parent / unquote(parsed.path)).resolve()
        resources.add(target)
        if not target.is_file():
            missing.add((str(source.relative_to(root)), value))
        elif target.suffix == '.css' and target not in stylesheets:
            stylesheets.add(target)
            pending.append(target)

    class Assets(HTMLParser):
        def __init__(self, source):
            super().__init__()
            self.source = source

        def handle_starttag(self, tag, attributes):
            attributes = dict(attributes)
            if tag in ('script', 'img', 'source'):
                reference(self.source, attributes.get('src', ''))
            elif tag == 'a' and 'gallery-link' in attributes.get('class', '').split():
                reference(self.source, attributes.get('href', ''))
            elif tag == 'link' and attributes.get('rel') in ('stylesheet', 'icon'):
                reference(self.source, attributes.get('href', ''))

    pages = list(root.rglob('*.html'))
    for page in pages:
        Assets(page).feed(page.read_text(encoding='utf-8'))
    while pending:
        css = pending.pop()
        text = css.read_text(encoding='utf-8')
        for match in re.finditer(r'url\(\s*[\'"]?([^\'"\)]+)[\'"]?\s*\)', text):
            reference(css, match[1].strip())
        for match in re.finditer(r'@import\s+[\'"]([^\'"]+)[\'"]', text):
            reference(css, match[1])
    return pages, stylesheets, resources, missing


if __name__ == '__main__':
    pages, stylesheets, resources, missing = check(ROOT)
    if missing:
        for source, value in sorted(missing):
            print('Missing asset:', source + ':', value, file=sys.stderr)
        sys.exit(1)
    print('Checked', len(pages), 'HTML pages,', len(stylesheets),
          'stylesheets and', len(resources), 'local assets; no missing files.')
