"""Protect native pages and the dependency chains of optional plugins."""
from pathlib import Path
import unittest
from page_dependencies import needs_jquery, prune

ROOT = Path(__file__).resolve().parents[1]


class PageDependencies(unittest.TestCase):
    def test_existing_pages_have_no_unnecessary_dependencies(self):
        for path in ROOT.rglob('*.html'):
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
        for path in ROOT.rglob('*.html'):
            updated = component_migrations.migrate(path, migrate(path, path.read_bytes()))
            self.assertEqual(prune(path, updated), updated, str(path))
