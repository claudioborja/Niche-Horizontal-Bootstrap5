#!/usr/bin/env python3
"""Create smaller lossless WebP copies, keeping original image URLs available.

Optional tooling: pip install -r tools/requirements-images.txt
The template and its checks do not require Pillow.
"""
from pathlib import Path
import io
import json
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]


def main():
    manifest = {}
    for source in sorted((ROOT / 'assets/img').rglob('*')):
        if source.suffix.lower() not in ('.jpg', '.jpeg', '.png'):
            continue
        with Image.open(source) as image:
            buffer = io.BytesIO()
            image.save(buffer, format='WEBP', lossless=True, exact=True, method=6)
            data = buffer.getvalue()
            if len(data) >= source.stat().st_size * .9:
                continue
            with Image.open(io.BytesIO(data)) as encoded:
                if image.convert('RGBA').tobytes() != encoded.convert('RGBA').tobytes():
                    raise ValueError('Image pixels changed: ' + str(source))
            target = source.with_suffix('.webp')
            if not target.exists() or target.read_bytes() != data:
                target.write_bytes(data)
            manifest[source.relative_to(ROOT).as_posix()] = {
                'target': target.relative_to(ROOT).as_posix(),
                'width': image.width, 'height': image.height,
                'before': source.stat().st_size, 'after': len(data),
            }
    output = ROOT / 'tools/image_optimization.json'
    data = json.dumps(manifest, indent=2, sort_keys=True) + '\n'
    if not output.exists() or output.read_text() != data:
        output.write_text(data)
    before = sum(item['before'] for item in manifest.values())
    after = sum(item['after'] for item in manifest.values())
    print(f'Optimized {len(manifest)} images without pixel changes: {before:,} -> {after:,} bytes ({(1 - after / before) * 100:.1f}% saved).' if before else 'No smaller lossless copies found.')


if __name__ == '__main__':
    main()
