"""Verify that screenshot comparisons detect pixel and dimension changes."""
import importlib.util
import asyncio
from pathlib import Path
import tempfile
import unittest

AVAILABLE = bool(importlib.util.find_spec('PIL') and importlib.util.find_spec('playwright'))


@unittest.skipUnless(AVAILABLE, 'Install tools/requirements-test.txt for visual tests')
class VisualComparison(unittest.TestCase):
    def setUp(self):
        from PIL import Image
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.left = Path(self.folder.name) / 'left.png'
        self.right = Path(self.folder.name) / 'right.png'
        Image.new('RGB', (10, 10), 'white').save(self.left)
        Image.new('RGB', (10, 10), 'white').save(self.right)

    def test_identical_pixels(self):
        from check_visual import compare
        self.assertEqual(compare(self.left, self.right)[0], 0)

    def test_pixel_changes_and_noise_threshold(self):
        from PIL import Image
        from check_visual import compare
        with Image.open(self.right) as image:
            image.putpixel((0, 0), (0, 0, 0))
            image.putpixel((1, 1), (250, 250, 250))
            image.save(self.right)
        self.assertEqual(compare(self.left, self.right)[0], .01)
        self.assertEqual(compare(self.left, self.right, threshold=0)[0], .02)

    def test_dimension_changes(self):
        from PIL import Image
        from check_visual import compare
        Image.new('RGB', (11, 10), 'white').save(self.right)
        self.assertEqual(compare(self.left, self.right), (1, None))

    def test_unknown_interactive_state_is_rejected(self):
        from check_visual import interactive_state
        with self.assertRaisesRegex(ValueError, 'Unknown interactive visual state'):
            asyncio.run(interactive_state(None, 'misspelled-state', 1440))
