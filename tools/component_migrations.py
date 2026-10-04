"""Migrate file inputs, editable tables and shared icons after vendor downloads."""
from pathlib import Path
import json
import re

FILEPOND = 'filepond-4.32.12'
TABULATOR = 'tabulator-6.6.1'
ICONS = 'bootstrap-icons-1.13.1'
CATALOGS = {'icon-fontawesome.html': 'all', 'icon-themify.html': 'interface',
            'icon-linea.html': 'arrows', 'icon-simple-lineicon.html': 'brands'}
# Keep legacy classes working for template styles and dynamic icon state changes.
ICON_MAP = {
    'fa-angle-right': 'chevron-right', 'fa-angle-left': 'chevron-left', 'fa-angle-down': 'chevron-down',
    'fa-arrow-right': 'arrow-right', 'fa-bell-o': 'bell', 'fa-book': 'book', 'fa-briefcase': 'briefcase',
    'fa-bullseye': 'bullseye', 'fa-camera': 'camera', 'fa-check': 'check', 'fa-check-square-o': 'check-square',
    'fa-chevron-left': 'chevron-left', 'fa-chevron-right': 'chevron-right', 'fa-circle': 'circle-fill',
    'fa-circle-o': 'circle', 'fa-clock-o': 'clock', 'fa-close': 'x-lg', 'fa-cloud-download': 'cloud-download',
    'fa-coffee': 'cup-hot', 'fa-credit-card': 'credit-card', 'fa-dashboard': 'speedometer2',
    'fa-download': 'download', 'fa-dropbox': 'dropbox', 'fa-edit': 'pencil-square',
    'fa-envelope': 'envelope-fill', 'fa-envelope-o': 'envelope', 'fa-facebook': 'facebook',
    'fa-file-pdf-o': 'file-earmark-pdf', 'fa-file-text-o': 'file-earmark-text', 'fa-file-word-o': 'file-earmark-word',
    'fa-files-o': 'files', 'fa-filter': 'funnel', 'fa-github': 'github', 'fa-globe': 'globe',
    'fa-google': 'google', 'fa-heart': 'heart-fill', 'fa-home': 'house', 'fa-inbox': 'inbox',
    'fa-info': 'info', 'fa-info-circle': 'info-circle', 'fa-instagram': 'instagram', 'fa-key': 'key',
    'fa-life-ring': 'life-preserver', 'fa-link': 'link-45deg', 'fa-linkedin': 'linkedin', 'fa-lock': 'lock',
    'fa-long-arrow-right': 'arrow-right', 'fa-magic': 'magic', 'fa-map-marker': 'geo-alt',
    'fa-minus': 'dash', 'fa-plus': 'plus', 'fa-paper-plane': 'send', 'fa-paperclip': 'paperclip',
    'fa-pencil': 'pencil', 'fa-phone': 'telephone', 'fa-plane': 'airplane', 'fa-power-off': 'power',
    'fa-print': 'printer', 'fa-refresh': 'arrow-clockwise', 'fa-reply': 'reply', 'fa-search': 'search',
    'fa-share': 'share', 'fa-sign-in': 'box-arrow-in-right', 'fa-square': 'square-fill', 'fa-square-o': 'square',
    'fa-star': 'star-fill', 'fa-star-o': 'star', 'fa-table': 'table', 'fa-th': 'grid-3x3-gap',
    'fa-thumbs-o-up': 'hand-thumbs-up', 'fa-times': 'x-lg', 'fa-trash-o': 'trash', 'fa-twitter': 'twitter',
    'fa-user': 'person', 'fa-user-plus': 'person-plus', 'fa-warning': 'exclamation-triangle',
    'icon-briefcase': 'briefcase', 'icon-circle': 'circle', 'icon-envelope': 'envelope',
    'icon-gears': 'gear', 'icon-layers': 'layers', 'icon-lightbulb': 'lightbulb', 'icon-pencil': 'pencil',
    'icon-profile-male': 'person', 'icon-wallet': 'wallet2',
    'ti-angle-down': 'chevron-down', 'ti-angle-right': 'chevron-right', 'ti-arrow-up': 'arrow-up',
    'ti-bar-chart': 'bar-chart', 'ti-close': 'x-lg', 'ti-email': 'envelope', 'ti-face-smile': 'emoji-smile',
    'ti-facebook': 'facebook', 'ti-google': 'google', 'ti-home': 'house', 'ti-lock': 'lock',
    'ti-money': 'cash-stack', 'ti-panel': 'layout-sidebar', 'ti-stats-up': 'graph-up',
    'ti-twitter-alt': 'twitter', 'ti-user': 'person', 'ti-wallet': 'wallet2', 'ti-world': 'globe',
}
BRANDS = ('bitbucket', 'flickr', 'foursquare', 'google-plus', 'tumblr', 'vk')


def icon_assets(root, css):
    """Generate compatibility rules from the downloaded font's actual code points."""
    points = dict(re.findall(r'\.bi-([\w-]+):{1,2}before\s*\{\s*content:\s*[\'"](\\[a-fA-F0-9]+)[\'"]', css))
    missing = set(ICON_MAP.values()) | {'list'}
    missing -= points.keys()
    if missing:
        raise ValueError('Missing Bootstrap Icons: ' + ', '.join(sorted(missing)))
    selectors = ['.fa::before'] + ['.' + name + '::before' for name in ICON_MAP if not name.startswith('fa-')]
    rules = [',\n'.join(selectors) + '{font-family:bootstrap-icons!important;font-style:normal;font-weight:normal!important;line-height:1;display:inline-block}',
             '.fa{display:inline-block;font-style:normal;font-weight:normal;line-height:1}',
             '.fa-fw{width:1.28571429em;text-align:center}.fa-lg{font-size:1.33333333em}.fa-2x{font-size:2em}.fa-3x{font-size:3em}.fa-4x{font-size:4em}.fa-5x{font-size:5em}',
             '.fa-ul{padding-left:0;margin-left:2.14285714em;list-style-type:none}.fa-ul>li{position:relative}.fa-li{position:absolute;left:-2.14285714em;width:2.14285714em;text-align:center}',
             '.fa-spin{animation:niche-icon-spin 2s infinite linear}@keyframes niche-icon-spin{to{transform:rotate(360deg)}}@media(prefers-reduced-motion:reduce){.fa-spin{animation:none}}']
    rules += ['.' + old + '::before{content:"' + points[new] + '"}' for old, new in ICON_MAP.items()]
    rules += ['.main-header .navbar-nav>li>a.sidebar-toggle{font-family:inherit}',
              '.main-header .sidebar-toggle::before{font-family:bootstrap-icons;content:"' + points['list'] + '"}']
    for brand in BRANDS:
        rules.append('.fa-' + brand + '::before{content:"";width:1em;height:1em;background:currentColor;vertical-align:-.125em;mask:url("../img/brands/' + brand + '.svg") center/contain no-repeat;-webkit-mask:url("../img/brands/' + brand + '.svg") center/contain no-repeat}')
    # Fetch the icon inventory from the same pinned package, rather than a second source.
    return {
        root / 'assets/css/icon-compat.css': ('/* Legacy class aliases for Bootstrap Icons; brand SVGs retain their original shapes. */\n' + '\n'.join(rules) + '\n').encode(),
        root / 'assets/js/icon-data.js': ('window.NicheIconNames = ' + json.dumps(sorted(points)) + ';\n').encode(),
    }


def migrate(path, original):
    if path.name == 'README.md':
        text = original.decode('utf-8')
        text = text.replace('La siguiente migración está preparada en el actualizador: FilePond 4.32.12\n'
                            'sustituye Dropify y Dropzone; Tabulator 6.6.1 sustituye jsGrid; Bootstrap Icons\n'
                            '1.13.1 unifica los iconos generales. Se aplica al ejecutar el script con acceso\n'
                            'a Internet, después de descargar y validar todos los recursos. Hasta entonces,\n'
                            'las páginas correspondientes siguen utilizando los componentes anteriores.',
                            'FilePond 4.32.12 sustituye Dropify y Dropzone; Tabulator 6.6.1 sustituye jsGrid;\n'
                            'Bootstrap Icons 1.13.1 unifica los iconos generales.')
        text = text.replace('[Font Awesome](icons/icon-fontawesome.html)', '[Bootstrap Icons](icons/icon-fontawesome.html)')
        if '| FilePond | 4.32.12 |' not in text:
            text = text.replace('| SheetJS | 0.20.3 | Exportación de tablas a XLSX, XLS, CSV y TXT |',
                                '| SheetJS | 0.20.3 | Exportación de tablas a XLSX, XLS, CSV y TXT |\n'
                                '| FilePond | 4.32.12 | Selección de archivos y adjuntos con vistas previas |\n'
                                '| Tabulator | 6.6.1 | Tablas editables, filtros y paginación local |\n'
                                '| Bootstrap Icons | 1.13.1 | Iconos generales y catálogos con búsqueda |')
        return text.encode('utf-8')
    if path.suffix != '.html':
        return original
    text = original.decode('utf-8')
    prefix = 'assets/' if (path.parent / 'assets').is_dir() else '../assets/'
    if path.name in CATALOGS:
        category = CATALOGS[path.name]
        content = '''<div class="content">
      <div class="info-box">
        <h4 class="text-black">Bootstrap Icons</h4>
        <label for="icon-search" class="form-label">Search icons</label>
        <input id="icon-search" class="form-control mb-3" type="search" placeholder="Search by name">
        <p id="icon-count" role="status"></p>
        <div id="icon-catalog" class="row g-3" data-category="%s"></div>
      </div>
    </div>
    ''' % category
        text = re.sub(r'<div class="content">.*?(?=<!-- /\.content -->)', lambda _: content, text, count=1, flags=re.S)
        text = re.sub(r'<link\b[^>]*href="[^"\n]*(?:lineaicon/styles\.css|simple-lineicon/simple-line-icons\.css)"[^>]*>\s*', '', text)
        if 'assets/js/icon-catalog.js' not in text:
            text = text.replace('</body>', '<script src="../assets/js/icon-data.js"></script>\n<script src="../assets/js/icon-catalog.js"></script>\n</body>')
    legacy = r'<link\b[^>]*href="[^"\n]*assets/css/(?:font-awesome/css/font-awesome\.min\.css|et-line-font/et-line-font\.css|themify-icons/themify-icons\.css)"[^>]*>[^\S\r\n]*\r?\n?'
    if re.search(legacy, text):
        replacement = '<link rel="stylesheet" href="' + prefix + 'plugins/' + ICONS + '/font/bootstrap-icons.min.css">\n<link rel="stylesheet" href="' + prefix + 'css/icon-compat.css">\n'
        text = re.sub(legacy, lambda match: replacement, text, count=1)
        text = re.sub(legacy, '', text)
    for old, new in [('Js Grid Table', 'Editable Tables'), ('Fontawesome Icons', 'Bootstrap Icons'),
                     ('Themify Icons', 'Interface Icons'), ('Linea Icons', 'Arrow Icons'), ('Simple Lineicons', 'Brand Icons')]:
        text = text.replace(old, new)
    if path.name in CATALOGS:
        for title in ('Font Awesome Icons', 'Font Awesome', 'Themify Icons', 'Linea Icons', 'Simple Line Icons', 'Simple Lineicons', 'Line Icons', 'Interface Icons', 'Arrow Icons', 'Brand Icons'):
            # Only update page headings/breadcrumb text; navigation already has distinct labels.
            text = re.sub(r'(<h1[^>]*>)' + re.escape(title) + r'(</h1>)', r'\1Bootstrap Icons\2', text)
    if path.name in ('form-uploads.html', 'apps-compose-mail.html'):
        text = re.sub(r'<link\b[^>]*href="[^"\n]*(?:dropify/dropify\.min\.css|dropzone-master/dropzone\.css)"[^>]*>',
                      '<link rel="stylesheet" href="../assets/plugins/' + FILEPOND + '/filepond.min.css">\n<link rel="stylesheet" href="../assets/plugins/filepond-plugin-image-preview-4.6.12/filepond-plugin-image-preview.min.css">', text)
        scripts = '\n'.join('<script src="../assets/' + asset + '"></script>' for asset in (
            'plugins/filepond-plugin-image-preview-4.6.12/filepond-plugin-image-preview.min.js',
            'plugins/filepond-plugin-file-validate-size-2.2.8/filepond-plugin-file-validate-size.min.js',
            'plugins/' + FILEPOND + '/filepond.min.js', 'js/file-uploads.js'))
        if path.name == 'form-uploads.html':
            text = text.replace('class="dropify"', 'class="filepond"').replace('data-default-file="assets/', 'data-default-file="../assets/').replace('data-max-file-size="2M"', 'data-max-file-size="2MB"')
            text = re.sub(r'<script src="../assets/plugins/dropify/dropify\.min\.js"></script>\s*<script>.*?</script>', lambda _: scripts, text, count=1, flags=re.S)
        else:
            text = re.sub(r'<form action="#" class="dropzone">.*?</form>', '<label for="mail-attachments" class="form-label">Choose attachments</label>\n<input id="mail-attachments" name="attachments" type="file" class="filepond" multiple>\n<p class="text-muted small">Files are selected locally. Sending requires a mail service.</p>', text, count=1, flags=re.S)
            text = text.replace('<script src="../assets/plugins/dropzone-master/dropzone.min.js"></script>', scripts)
    if path.name == 'table-jsgrid.html':
        text = re.sub(r'<link\b[^>]*href="[^"\n]*jsgrid/(?:jsgrid(?:\.theme)?|theme)\.css"[^>]*>\s*', '', text)
        if 'tabulator_bootstrap5.min.css' not in text:
            text = text.replace('</head>', '<link rel="stylesheet" href="../assets/plugins/' + TABULATOR + '/css/tabulator_bootstrap5.min.css">\n</head>')
        text = text.replace('Editable with Datatable', 'Editable table with filters').replace('>Soarting<', '>Sorting<')
        if 'for="sortingField"' not in text:
            text = text.replace('<select id="sortingField"', '<label for="sortingField" class="form-label">Sort by</label>\n<select id="sortingField"')
        text = text.replace('custom-select form-control input-sm', 'form-select')
        text = text.replace('<script src="../assets/plugins/jsgrid/db.js"></script>', '<script src="../assets/js/grid-data.js"></script>')
        text = text.replace('<script src="../assets/plugins/jsgrid/jsgrid.min.js"></script>', '<script src="../assets/plugins/' + TABULATOR + '/js/tabulator.min.js"></script>')
        text = text.replace('<script src="../assets/plugins/jsgrid/jsgrid.int.js"></script>', '<script src="../assets/js/editable-tables.js"></script>')
    return text.encode('utf-8')
