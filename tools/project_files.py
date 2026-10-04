"""Find template pages without entering optional tooling or generated reports."""
import os
from pathlib import Path

EXCLUDED_DIRECTORIES = {'.git', '.venv', 'node_modules', '__pycache__',
                        'visual-results', 'performance-results'}


def html_pages(root):
    for directory, subdirectories, filenames in os.walk(root):
        subdirectories[:] = [name for name in subdirectories if name not in EXCLUDED_DIRECTORIES]
        for name in filenames:
            if name.endswith('.html'):
                yield Path(directory) / name
