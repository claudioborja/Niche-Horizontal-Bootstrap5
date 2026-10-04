#!/usr/bin/env python3
"""Stage pinned vendor downloads and page migrations before applying them."""
from pathlib import Path
from html.parser import HTMLParser
import re
import sys
import tempfile
import urllib.request
import urllib.error
import component_migrations
import legacy_widget_migrations

ROOT = Path(__file__).resolve().parents[1]
# Each asset has its own content marker; small CSS/integration files are valid.
UPDATES = (
    ('poppins', 'poppins-5.3.0', tuple(
        (str(weight) + '.css', 'https://cdn.jsdelivr.net/npm/@fontsource/poppins@5.3.0/' + str(weight) + '.css', b"font-family: 'Poppins'")
        for weight in (300, 400, 500, 600, 700)
    ) + tuple(
        ('files/poppins-' + subset + '-' + str(weight) + '-normal.woff2',
         'https://cdn.jsdelivr.net/npm/@fontsource/poppins@5.3.0/files/poppins-' + subset + '-' + str(weight) + '-normal.woff2', b'wOF2')
        for weight in (300, 400, 500, 600, 700) for subset in ('devanagari', 'latin-ext', 'latin')
    ) + (('LICENSE', 'https://cdn.jsdelivr.net/npm/@fontsource/poppins@5.3.0/LICENSE', b'SIL OPEN FONT LICENSE'),)),
    ('jodit', 'jodit-4.17.1', (
        ('jodit.min.js', 'https://cdn.jsdelivr.net/npm/jodit@4.17.1/es2021/jodit.min.js', b'Version: v4.17.1'),
        ('jodit.min.css', 'https://cdn.jsdelivr.net/npm/jodit@4.17.1/es2021/jodit.min.css', b'.jodit-'),
        ('LICENSE.txt', 'https://cdn.jsdelivr.net/npm/jodit@4.17.1/LICENSE.txt', b'Permission is hereby granted'),
    )),
    ('jquery-3.7.1', 'jquery-4.0.0', (
        ('jquery.min.js', 'https://cdn.jsdelivr.net/npm/jquery@4.0.0/dist/jquery.min.js', b'jQuery v4.0.0'),
    )),
    ('ion-rangeslider', 'ion-rangeslider-2.5.0', (
        ('ion.rangeSlider.min.js', 'https://cdn.jsdelivr.net/npm/ion-rangeslider@2.5.0/js/ion.rangeSlider.min.js', b'Ion.RangeSlider, 2.5.0'),
        ('ion.rangeSlider.css', 'https://cdn.jsdelivr.net/npm/ion-rangeslider@2.5.0/css/ion.rangeSlider.min.css', b'.irs'),
    )),
    ('bootstrap-5.3.2', 'bootstrap-5.3.8', (
        ('css/bootstrap.min.css', 'https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css', b'Bootstrap v5.3.8'),
        ('js/bootstrap.min.js', 'https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/js/bootstrap.min.js', b'Bootstrap v5.3.8'),
    )),
    ('chart-js-4.4.0', 'chart-js-4.5.1', (
        ('chart.umd.js', 'https://cdn.jsdelivr.net/npm/chart.js@4.5.1/dist/chart.umd.js', b'Chart.js v4.5.1'),
    )),
    ('jquery-ui', 'jquery-ui', (
        ('jquery-ui.min.js', 'https://code.jquery.com/ui/1.14.2/jquery-ui.min.js', b'jQuery UI - v1.14.2'),
    )),
    ('datatables', 'datatables-3.1.3', (
        ('dataTables.min.js', 'https://cdn.jsdelivr.net/npm/datatables.net@3.1.3/js/dataTables.min.js', b'3.1.3'),
        ('dataTables.bootstrap5.min.js', 'https://cdn.jsdelivr.net/npm/datatables.net-bs5@3.1.3/js/dataTables.bootstrap5.min.js', b'DataTables'),
        ('css/dataTables.bootstrap5.min.css', 'https://cdn.jsdelivr.net/npm/datatables.net-bs5@3.1.3/css/dataTables.bootstrap5.min.css', b'.dt-'),
    )),
    ('fullcalendar-6.1.21', 'fullcalendar-7.1.0', (
        ('js/fullcalendar.min.js', 'https://cdn.jsdelivr.net/npm/fullcalendar@7.1.0/all/global.min.js', b'v7.1.0'),
        ('css/skeleton.css', 'https://cdn.jsdelivr.net/npm/fullcalendar@7.1.0/skeleton.css', b'fc-'),
        ('js/bootstrap5.js', 'https://cdn.jsdelivr.net/npm/@fullcalendar/bootstrap5@7.1.0/global.min.js', b'v7.1.0'),
        ('css/bootstrap5.css', 'https://cdn.jsdelivr.net/npm/@fullcalendar/bootstrap5@7.1.0/theme.css', b'.fc-bootstrap5-'),
    )),
    ('jquery-validation', 'jquery-validation-1.22.1', (
        ('jquery.validate.min.js', 'https://cdn.jsdelivr.net/npm/jquery-validation@1.22.1/dist/jquery.validate.min.js', b'v1.22.1'),
    )),
    ('sheetjs', 'sheetjs-0.20.3', (
        ('xlsx.full.min.js', 'https://cdn.sheetjs.com/xlsx-0.20.3/package/dist/xlsx.full.min.js', b'0.20.3'),
    )),
    ('filepond', 'filepond-4.32.12', (
        ('filepond.min.js', 'https://cdn.jsdelivr.net/npm/filepond@4.32.12/dist/filepond.min.js', b'FilePond'),
        ('filepond.min.css', 'https://cdn.jsdelivr.net/npm/filepond@4.32.12/dist/filepond.min.css', b'.filepond--'),
    )),
    ('filepond-plugin-image-preview', 'filepond-plugin-image-preview-4.6.12', (
        ('filepond-plugin-image-preview.min.js', 'https://cdn.jsdelivr.net/npm/filepond-plugin-image-preview@4.6.12/dist/filepond-plugin-image-preview.min.js', b'FilePondPluginImagePreview'),
        ('filepond-plugin-image-preview.min.css', 'https://cdn.jsdelivr.net/npm/filepond-plugin-image-preview@4.6.12/dist/filepond-plugin-image-preview.min.css', b'.filepond--image-preview'),
    )),
    ('filepond-plugin-file-validate-size', 'filepond-plugin-file-validate-size-2.2.8', (
        ('filepond-plugin-file-validate-size.min.js', 'https://cdn.jsdelivr.net/npm/filepond-plugin-file-validate-size@2.2.8/dist/filepond-plugin-file-validate-size.min.js', b'FilePondPluginFileValidateSize'),
    )),
    ('tabulator', 'tabulator-6.6.1', (
        ('js/tabulator.min.js', 'https://cdn.jsdelivr.net/npm/tabulator-tables@6.6.1/dist/js/tabulator.min.js', b'Tabulator'),
        ('css/tabulator_bootstrap5.min.css', 'https://cdn.jsdelivr.net/npm/tabulator-tables@6.6.1/dist/css/tabulator_bootstrap5.min.css', b'.tabulator'),
    )),
    ('bootstrap-icons', 'bootstrap-icons-1.13.1', (
        ('font/bootstrap-icons.min.css', 'https://cdn.jsdelivr.net/npm/bootstrap-icons@1.13.1/font/bootstrap-icons.min.css', b'bootstrap-icons'),
        ('font/fonts/bootstrap-icons.woff2', 'https://cdn.jsdelivr.net/npm/bootstrap-icons@1.13.1/font/fonts/bootstrap-icons.woff2', b'wOF2'),
        ('font/fonts/bootstrap-icons.woff', 'https://cdn.jsdelivr.net/npm/bootstrap-icons@1.13.1/font/fonts/bootstrap-icons.woff', b'wOFF'),
    )),
)


def validate(data, marker, url):
    normalized = b' '.join(data.split())
    if len(data) < 200 or data.lstrip().lower().startswith((b'<!doctype html', b'<html')) or (marker and marker not in normalized):
        raise ValueError('Unexpected vendor content: ' + url + ' (expected '
                         + repr(marker) + ', received ' + str(len(data)) + ' bytes)')


def download(url, marker):
    candidates = [url]
    if url.startswith('https://cdn.jsdelivr.net/npm/'):
        candidates.append(url.replace('https://cdn.jsdelivr.net/npm/', 'https://unpkg.com/', 1))
    errors = []
    for candidate in candidates:
        print('Downloading', candidate, flush=True)
        try:
            request = urllib.request.Request(candidate, headers={
                'User-Agent': 'Niche-Dependency-Updater/1.0',
                'Accept': '*/*',
            })
            with urllib.request.urlopen(request, timeout=30) as response:
                data = response.read()
            validate(data, marker, candidate)
            return data
        except (urllib.error.URLError, ValueError, TimeoutError) as error:
            errors.append(candidate + ': ' + str(error))
            if candidate != candidates[-1]:
                print('Source unavailable; trying the same pinned package on UNPKG.', flush=True)
    raise RuntimeError('Could not download dependency:\n' + '\n'.join(errors))


class AssetReferences(HTMLParser):
    def __init__(self):
        super().__init__()
        self.references = []

    def handle_starttag(self, tag, attributes):
        attributes = dict(attributes)
        if tag == 'script' and attributes.get('src'):
            self.references.append(attributes['src'])
        elif tag == 'link' and attributes.get('rel') == 'stylesheet' and attributes.get('href'):
            self.references.append(attributes['href'])


def migrate(path, original):
    updated = original
    if path.suffix == '.html':
        prefix = b'assets/' if path.parent == ROOT else b'../assets/'
        updated = re.sub(rb'https://fonts\.googleapis\.com/[^"\s]+', prefix + b'plugins/poppins-5.3.0/poppins.css', updated)
        # FullCalendar v6 injects its own styles; these old files contain a CDN error.
        updated = re.sub(rb'<link\b[^>]*href="[^"\n]*fullcalendar-6\.1\.(?:8|21)/css/fullcalendar\.min\.css"[^>]*>[^\S\r\n]*\r?\n', b'', updated)
        updated = updated.replace(b'assets/plugins/fullcalendar-6.1.8/', b'assets/plugins/fullcalendar-6.1.21/')
        updated = re.sub(rb'<link\b[^>]*href="[^"\n]*ion-rangeslider(?:-2\.5\.0)?/ion\.rangeSlider\.skinModern\.css"[^>]*>[^\S\r\n]*\r?\n', b'', updated)
        for old, new, _ in UPDATES:
            if old != new:
                updated = updated.replace(('assets/plugins/' + old + '/').encode(), ('assets/plugins/' + new + '/').encode())
        if path.name == 'ui-range-slider.html':
            updated = re.sub(rb'(<h4[^>]*)(>[^<]*</h4>\s*)<div id="(range_\d+)"></div>',
                             lambda m: m[1] + b' id="' + m[3] + b'-label"' + m[2]
                             + b'<input type="text" id="' + m[3] + b'" aria-labelledby="' + m[3] + b'-label">', updated)
        calendar_script = b'<script src="../assets/plugins/fullcalendar-7.1.0/js/fullcalendar.min.js"></script>'
        if calendar_script in updated:
            if b'fullcalendar-7.1.0/css/skeleton.css' not in updated:
                updated = updated.replace(b'<!-- Calendar -->', b'<!-- Calendar -->\n<link rel="stylesheet" href="../assets/plugins/fullcalendar-7.1.0/css/skeleton.css">\n<link rel="stylesheet" href="../assets/plugins/fullcalendar-7.1.0/css/bootstrap5.css">', 1)
            if b'fullcalendar-7.1.0/js/bootstrap5.js' not in updated:
                updated = updated.replace(calendar_script, calendar_script + b'\n<script src="../assets/plugins/fullcalendar-7.1.0/js/bootstrap5.js"></script>')
        updated = updated.replace(b'datatables-3.1.3/jquery.dataTables.min.js', b'datatables-3.1.3/dataTables.min.js')
        updated = updated.replace(b'https://cdnjs.cloudflare.com/ajax/libs/jquery-validate/1.16.0/jquery.validate.min.js', b'../assets/plugins/jquery-validation-1.22.1/jquery.validate.min.js')
        updated = updated.replace(b"$('#example1').DataTable()", b"if (document.getElementById('example1')) new DataTable('#example1', { deferRender: false })")
        updated = updated.replace(b"$('#example2').DataTable({", b"if (document.getElementById('example2')) new DataTable('#example2', {\n      'deferRender': false,")
        if path == ROOT / 'tables/table-data-table.html':
            updated = re.sub(rb'<script src="../assets/plugins/table-expo/(?:filesaver\.min\.js|xls\.core\.min\.js)"></script>[^\S\r\n]*\r?\n', b'', updated)
            updated = updated.replace(b'../assets/plugins/table-expo/tableexport.js', b'../assets/plugins/sheetjs-0.20.3/xlsx.full.min.js')
            updated = re.sub(rb'<script>\s*\$\("table"\)\.tableExport\([^<]*</script>', b'<script src="../assets/js/table-export.js"></script>', updated)
        updated = updated.replace(b'Bootstrap 5.3.2', b'Bootstrap 5.3.8')
        updated = updated.replace(b'<!-- jQuery 3 -->', b'<!-- jQuery 4 -->').replace(b'<!-- jQuery UI 1.11.4 -->', b'<!-- jQuery UI 1.14.2 -->')
        lines = updated.splitlines(keepends=True)
        previous = original.splitlines(keepends=True)
        # Only clean newly changed lines; preserve untouched formatting.
        if len(lines) == len(previous):
            updated = b''.join(line.rstrip(b' \t\r\n') + (b'\r\n' if line.endswith(b'\r\n') else b'\n' if line.endswith(b'\n') else b'')
                               if line != old else line for old, line in zip(previous, lines))
    elif path.name == 'README.md':
        for old, new, _ in UPDATES:
            updated = updated.replace((old + '/').encode(), (new + '/').encode())
        updated = updated.replace(b'| jQuery | 3.7.1 |', b'| jQuery | 4.0.0 |').replace(b'| FullCalendar | 6.1.21 |', b'| FullCalendar | 7.1.0 |')
        for old, new in [
            (b'DataTables 1.10.15', b'DataTables 3.1.3'),
            (b' (migraci\xc3\xb3n pendiente)', b''),
            (b'Bootstrap 5.3.2', b'Bootstrap 5.3.8'),
            (b'Chart.js 4.4.0', b'Chart.js 4.5.1'),
            (b'**Bootstrap:** 5.3.2', b'**Bootstrap:** 5.3.8'),
            (b'- **FullCalendar**', b'- **FullCalendar 6.1.21**'),
            (b'- **Summernote**', b'- **Summernote 0.9.1**'),
        ]:
            updated = updated.replace(old, new)
    return legacy_widget_migrations.migrate(path, updated)


def main():
    with tempfile.TemporaryDirectory(prefix='niche-dependencies-') as directory:
        staged = {}

        def stage(relative, url, marker):
            target = ROOT / 'assets/plugins' / relative
            if target.exists():
                data = target.read_bytes()
                try:
                    validate(data, marker, url)
                    print('Already installed:', relative, flush=True)
                    staged[target] = data
                    return data
                except ValueError:
                    pass
            data = download(url, marker)
            cached = Path(directory) / relative
            cached.parent.mkdir(parents=True, exist_ok=True)
            cached.write_bytes(data)
            staged[target] = data
            return data

        for _, target, files in UPDATES:
            for filename, url, marker in files:
                stage(target + '/' + filename, url, marker)

        font_dir = ROOT / 'assets/plugins/poppins-5.3.0'
        font_css = []
        for weight in (300, 400, 500, 600, 700):
            css = staged[font_dir / (str(weight) + '.css')].decode('utf-8')
            css = re.sub(r", url\([^)]*\.woff\) format\('woff'\)", '', css)
            font_css.append(css)
        staged[font_dir / 'poppins.css'] = ('/* Poppins via Fontsource 5.3.0; see LICENSE. */\n' + '\n\n'.join(font_css)).encode('utf-8')

        icon_css = staged[ROOT / 'assets/plugins/bootstrap-icons-1.13.1/font/bootstrap-icons.min.css']
        staged.update(component_migrations.icon_assets(ROOT, icon_css.decode('utf-8')))

        for path in list(ROOT.rglob('*.html')) + [ROOT / 'README.md']:
            original = path.read_bytes()
            updated = migrate(path, original)
            updated = component_migrations.migrate(path, updated)
            if updated != original:
                staged[path] = updated

        pages = list(ROOT.rglob('*.html'))
        for path in pages:
            parser = AssetReferences()
            parser.feed(staged.get(path, path.read_bytes()).decode('utf-8'))
            for reference in parser.references:
                if reference.startswith(('http:', 'https:', '//', 'data:')):
                    continue
                target = (path.parent / reference.split('?')[0]).resolve()
                if target not in staged and not target.is_file():
                    raise ValueError('Missing local asset after migration: ' + str(path) + ': ' + reference)

        # All downloads and migrations succeed before changing installed files.
        backups = {path: path.read_bytes() if path.exists() else None for path in staged}
        written = []
        try:
            for path, data in staged.items():
                if backups[path] == data:
                    continue
                path.parent.mkdir(parents=True, exist_ok=True)
                written.append(path)
                path.write_bytes(data)
        except OSError:
            for path in reversed(written):
                if backups[path] is None:
                    path.unlink(missing_ok=True)
                else:
                    path.write_bytes(backups[path])
            raise
        print('Updated Bootstrap 5.3.8, Chart.js 4.5.1, jQuery UI 1.14.2, DataTables 3.1.3, '
              'jQuery 4.0.0, Ion.RangeSlider 2.5.0, FullCalendar 7.1.0, Jodit 4.17.1, jQuery Validation 1.22.1, SheetJS 0.20.3, '
              'FilePond 4.32.12, Tabulator 6.6.1, Bootstrap Icons 1.13.1 and local Poppins (Fontsource 5.3.0).')
        print('Checked local JavaScript and CSS references in', len(pages), 'HTML pages.')


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        print('Update failed: ' + str(error), file=sys.stderr)
        sys.exit(1)
