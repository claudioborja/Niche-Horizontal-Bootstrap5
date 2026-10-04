#!/usr/bin/env python3
"""Verify staged migrations without downloading or changing installed assets."""
import contextlib
import io
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import component_migrations as components
import update_dependencies as updater

ROOT = Path(__file__).resolve().parents[1]


def font_fixture():
    # Test font declarations, deliberately mixing minified and unminified syntax.
    return '\n'.join('.bi-' + name + (':before{content:"\\f101"}' if i % 2 else '::before { content: "\\f102"; }')
                     for i, name in enumerate(sorted(set(components.ICON_MAP.values()) | {'list'})))


class Migrations(unittest.TestCase):
    def test_every_page_can_migrate_twice(self):
        for path in list(ROOT.rglob('*.html')) + [ROOT / 'README.md']:
            first = components.migrate(path, updater.migrate(path, path.read_bytes()))
            self.assertEqual(components.migrate(path, first), first, str(path))

    def test_previews_and_upload_options(self):
        path = ROOT / 'forms/form-uploads.html'
        text = components.migrate(path, path.read_bytes()).decode()
        self.assertEqual(text.count('class="filepond"'), 8)
        self.assertIn('data-max-file-size="2MB"', text)
        self.assertIn('data-show-remove="false"', text)
        self.assertEqual(text.count('disabled="disabled"'), 2)
        for name in ('img13.jpg', 'img14.jpg', 'img15.jpg'):
            self.assertIn('data-default-file="../assets/img/' + name + '"', text)
            self.assertTrue((ROOT / 'assets/img' / name).is_file())
        self.assertNotIn(".dropify(", text)

    def test_mail_attachments_remain_local(self):
        path = ROOT / 'apps/apps-compose-mail.html'
        text = components.migrate(path, path.read_bytes()).decode()
        self.assertIn('class="filepond" multiple', text)
        self.assertNotIn('class="dropzone"', text)
        self.assertNotIn('dropzone.min.js', text)

    def test_table_migration(self):
        path = ROOT / 'tables/table-jsgrid.html'
        text = components.migrate(path, path.read_bytes()).decode()
        self.assertIn('tabulator_bootstrap5.min.css', text)
        self.assertNotIn('assets/plugins/jsgrid/', text)
        self.assertEqual(text.count('for="sortingField"'), 1)
        self.assertIn('id="soarting"', text)  # Existing initializer target remains stable.

    def test_incomplete_icon_font_is_rejected(self):
        with self.assertRaises(ValueError):
            components.icon_assets(ROOT, '.bi-list:before{content:"\\f101"}')
        assets = components.icon_assets(ROOT, font_fixture())
        rules = assets[ROOT / 'assets/css/icon-compat.css'].decode()
        for brand in components.BRANDS:
            self.assertIn('../img/brands/' + brand + '.svg', rules)
            self.assertTrue((ROOT / 'assets/img/brands' / (brand + '.svg')).is_file())

    def test_download_failure_preserves_installed_files(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            page = root / 'index.html'
            page.write_text('<html>Original page</html>')
            (root / 'README.md').write_text('Original README')
            with patch.object(updater, 'ROOT', root), patch.object(updater, 'download', side_effect=RuntimeError('DNS failure')):
                with contextlib.redirect_stdout(io.StringIO()), self.assertRaises(RuntimeError):
                    updater.main()
            self.assertEqual(page.read_text(), '<html>Original page</html>')
            self.assertEqual((root / 'README.md').read_text(), 'Original README')
            self.assertFalse((root / 'assets').exists())

    def test_successful_staging_checks_all_page_routes(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for source in list(ROOT.rglob('*.html')) + [ROOT / 'README.md']:
                target = root / source.relative_to(ROOT)
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(source.read_bytes())
            # Existing non-updated resources are placeholders in this isolated fixture.
            # Newly migrated helper references are created separately below.
            for page in root.rglob('*.html'):
                parser = updater.AssetReferences()
                parser.feed(page.read_text())
                for reference in parser.references:
                    if reference.startswith(('http:', 'https:', '//', 'data:')):
                        continue
                    target = (page.parent / reference.split('?')[0]).resolve()
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes(b'existing asset fixture' * 20)
            for name in ('file-uploads', 'editable-tables', 'grid-data', 'icon-catalog'):
                (root / 'assets/js' / (name + '.js')).write_bytes((ROOT / 'assets/js' / (name + '.js')).read_bytes())
            def fake_download(url, marker):
                if url.endswith('font/bootstrap-icons.min.css'):
                    return ('/* bootstrap-icons */\n' + font_fixture()).encode()
                return (marker or b'font fixture') + b' ' * 300
            with patch.object(updater, 'ROOT', root), patch.object(updater, 'download', side_effect=fake_download):
                with contextlib.redirect_stdout(io.StringIO()):
                    updater.main()
            pages = list(root.rglob('*.html'))
            self.assertEqual(len(pages), 67)
            for page in pages:
                text = page.read_text()
                self.assertNotIn('font-awesome/css/font-awesome.min.css', text)
                self.assertNotIn('assets/plugins/jsgrid/', text)
                self.assertEqual(components.migrate(page, page.read_bytes()), page.read_bytes(), str(page))
            self.assertIn('| FilePond | 4.32.12 |', (root / 'README.md').read_text())
            self.assertNotIn('migración está preparada', (root / 'README.md').read_text())
            self.assertTrue((root / 'assets/css/icon-compat.css').is_file())
            self.assertTrue((root / 'assets/js/icon-data.js').is_file())


if __name__ == '__main__':
    unittest.main()
