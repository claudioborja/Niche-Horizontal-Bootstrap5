from pathlib import Path
import tempfile
import unittest

from project_files import html_pages


class ProjectFiles(unittest.TestCase):
    def test_optional_tools_and_reports_are_not_template_pages(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name in ('index.html', 'pages/example.html',
                         'tools/lighthouse/node_modules/vendor/template.html',
                         'tools/performance-results/report.html', '.venv/example.html'):
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text('<html></html>')
            self.assertEqual({path.relative_to(root).as_posix() for path in html_pages(root)},
                             {'index.html', 'pages/example.html'})
