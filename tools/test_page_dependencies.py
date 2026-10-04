"""Protect native pages and the dependency chains of optional plugins."""
from project_files import html_pages
from pathlib import Path
import unittest
from page_dependencies import needs_jquery, prune

ROOT = Path(__file__).resolve().parents[1]


class PageDependencies(unittest.TestCase):
    def test_icon_inventory_is_preserved_for_catalogs_and_custom_icons(self):
        link = b'<link href="assets/plugins/bootstrap-icons-1.13.1/font/bootstrap-icons.min.css" rel="stylesheet">'
        small = prune(Path('index.html'), link)
        self.assertIn(b'bootstrap-icons-font.css', small)
        self.assertEqual(prune(Path('index.html'), small), small)
        for extra in (b'<i class="bi bi-star"></i>', b'<script src="assets/js/icon-catalog.js"></script>',
                      b'<script src="assets/plugins/fullcalendar-7.1.0/js/bootstrap5.js"></script>'):
            self.assertEqual(prune(Path('icons.html'), link + extra), link + extra)
            self.assertEqual(prune(Path('icons.html'), small + extra), link + extra)

    def test_existing_pages_have_no_unnecessary_dependencies(self):
        for path in html_pages(ROOT):
            original = path.read_bytes()
            self.assertEqual(prune(path, original), original, str(path))
            text = original.decode()
            self.assertEqual('jquery-4.0.0/jquery.min.js' in text, needs_jquery(text), str(path))

    def test_unknown_integrations_keep_jquery(self):
        html = b'<script src="assets/plugins/jquery-4.0.0/jquery.min.js"></script>\n<script src="assets/js/custom-widget.js"></script>'
        self.assertEqual(prune(Path('custom.html'), html), html)

    def test_updater_does_not_restore_removed_loads(self):
        from update_dependencies import migrate
        import component_migrations
        for path in html_pages(ROOT):
            updated = component_migrations.migrate(path, migrate(path, path.read_bytes()))
            self.assertEqual(prune(path, updated), updated, str(path))
