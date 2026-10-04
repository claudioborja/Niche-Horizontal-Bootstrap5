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
            self.assertEqual(components.migrate(path, updater.migrate(path, first)), first, str(path))

    def test_calendar_v7_dependencies_are_ordered_and_unique(self):
        text = updater.migrate(ROOT / 'apps/apps-calendar.html', (ROOT / 'apps/apps-calendar.html').read_bytes()).decode()
        self.assertEqual(text.count('fullcalendar-7.1.0/css/skeleton.css'), 1)
        self.assertEqual(text.count('fullcalendar-7.1.0/css/bootstrap5.css'), 1)
        self.assertLess(text.index('fullcalendar-7.1.0/js/fullcalendar.min.js'), text.index('fullcalendar-7.1.0/js/bootstrap5.js'))
        self.assertLess(text.index('fullcalendar-7.1.0/js/bootstrap5.js'), text.index('functions/calendar-init.js'))

    def test_jquery_bridge_is_removed_and_not_reinstalled(self):
        for path in ROOT.rglob('*.html'):
            text = updater.migrate(path, path.read_bytes()).decode()
            self.assertNotIn('jquery-3.7.1/', text)
            self.assertNotIn('jquery-migrate', text, str(path))
        self.assertFalse(any('jquery-migrate' in target for _, target, _ in updater.UPDATES))

    def test_google_fonts_migrates_to_local_typography_at_both_depths(self):
        old = b'<link href="https://fonts.googleapis.com/css?family=Poppins:300,400,500,600,700" rel="stylesheet">'
        for relative, prefix in [('index.html', b'assets/'), ('pages/pages-login.html', b'../assets/')]:
            path = ROOT / relative
            result = updater.migrate(path, old)
            self.assertIn(prefix + b'plugins/poppins-5.3.0/poppins.css', result)
            self.assertNotIn(b'fonts.googleapis', result)
            self.assertEqual(updater.migrate(path, result), result)

    def test_native_core_removes_vendor_menu_and_keeps_one_optional_bridge(self):
        old = b'''<script src="assets/plugins/jquery-4.0.0/jquery.min.js"></script>
<script src="assets/js/custom-jquery-integration.js"></script>
<script src="assets/js/niche/widgets.js"></script>
<script src="assets/plugins/hmenu/ace-responsive-menu.js"></script>
<script src="assets/plugins/jquery-slimscroll/jquery.slimscroll.min.js"></script>'''
        path = ROOT / 'index.html'
        result = updater.migrate(path, old)
        self.assertNotIn(b'ace-responsive-menu.js', result)
        self.assertNotIn(b'jquery-slimscroll', result)
        self.assertEqual(result.count(b'niche/jquery-bridge.js'), 1)
        self.assertLess(result.index(b'niche/widgets.js'), result.index(b'niche/jquery-bridge.js'))
        self.assertEqual(updater.migrate(path, result), result)

    def test_range_sliders_use_labelled_inputs(self):
        text = updater.migrate(ROOT / 'ui/ui-range-slider.html', (ROOT / 'ui/ui-range-slider.html').read_bytes()).decode()
        self.assertNotIn('skinModern.css', text)
        for number in ('01', '02', '03', '04', '16', '18', '22'):
            self.assertIn('type="text" id="range_' + number + '" aria-labelledby="range_' + number + '-label"', text)
            self.assertIn('id="range_' + number + '-label"', text)

    def test_legacy_editor_is_replaced_without_losing_initial_content(self):
        path = ROOT / 'apps/apps-compose-mail.html'
        old = b'''<link rel="stylesheet" href="../assets/plugins/summernote-0.9.1/summernote-bs5.min.css">
<textarea id="compose-textarea" class="form-control"><p>Initial message</p></textarea>
<script src="../assets/plugins/jquery-migrate-4.0.2/jquery-migrate.min.js"></script>
<script src="../assets/plugins/summernote-0.9.1/summernote-bs5.min.js"></script>'''
        text = updater.migrate(path, old)
        self.assertIn(b'<p>Initial message</p>', text)
        self.assertIn(b'jodit-4.17.1/jodit.min.js', text)
        self.assertIn(b'jodit-4.17.1/jodit.min.css', text)
        self.assertNotIn(b'jquery-migrate', text)
        self.assertNotIn(b'summernote-0.9.1', text)
        self.assertEqual(updater.migrate(path, text), text)

    def test_mini_chart_migration_preserves_values_and_dimensions(self):
        path = ROOT / 'index3.html'
        old = b'''<head></head><span class="bar" data-peity='{ "fill": ["#f96262", "#f2f2f2"]}' data-width="100%" data-height="60">5,3,2,-1,-3</span>
<script src="assets/plugins/peity/jquery.peity.min.js"></script>
<script src="assets/plugins/functions/jquery.peity.init.js"></script>'''
        text = updater.migrate(path, old)
        for value in (b'data-mini-chart="bar"', b'data-values="5,3,2,-1,-3"', b'data-width="100%"', b'data-height="60"', b'#f96262'):
            self.assertIn(value, text)
        self.assertNotIn(b'plugins/peity/', text)
        self.assertEqual(text.count(b'chart-js-4.5.1/chart.umd.js'), 1)
        self.assertLess(text.index(b'chart.umd.js'), text.index(b'js/mini-charts.js'))
        self.assertEqual(updater.migrate(path, text), text)

    def test_gallery_migration_preserves_combined_categories_and_links(self):
        path = ROOT / 'pages/pages-gallery.html'
        old = b'''<body><div id="js-filters-masonry" class="cbp-l-filters-alignRight">
<div data-filter=".graphic, .identity" class="cbp-filter-item">Combined<div class="cbp-filter-counter"></div></div></div>
<div id="js-grid-masonry" class="cbp"><div class="cbp-item graphic identity"><a class="cbp-caption cbp-lightbox" href="image.jpg">Image</a></div></div></body>'''
        text = updater.migrate(path, old)
        self.assertIn(b'<button type="button" data-filter=".graphic, .identity"', text)
        self.assertIn(b'class="gallery-item graphic identity"', text)
        self.assertIn(b'href="image.jpg"', text)
        self.assertEqual(text.count(b'id="gallery-lightbox"'), 1)
        self.assertNotIn(b'cbp', text)
        self.assertEqual(updater.migrate(path, text), text)

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
