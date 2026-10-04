"""Keep demo authentication local and preserve component attributes."""
from pathlib import Path
import unittest
from demo_migrations import migrate


class DemoMigrations(unittest.TestCase):
    def test_auth_form_keeps_attributes_and_removes_endpoint(self):
        path = Path('pages/pages-login.html')
        source = b'<form id="login" class="custom" action="../index.html" method="post"></form></body>'
        result = migrate(path, source)
        self.assertIn(b'id="login" class="custom"', result)
        self.assertIn(b'data-demo-form="true"', result)
        self.assertNotIn(b'method=', result)
        self.assertNotIn(b'action=', result)
        self.assertEqual(migrate(path, result), result)

    def test_home_routes_work_at_both_depths(self):
        for path, target in ((Path('index.html'), b'index.html'), (Path('pages/pages-blank.html'), b'../index.html')):
            result = migrate(path, b'<a href="#">Home</a></body>')
            self.assertIn(b'href="' + target + b'"', result)
            self.assertEqual(result.count(b'js/demo-actions.js'), 1)
