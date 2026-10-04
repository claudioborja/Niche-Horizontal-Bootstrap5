"""Replace legacy editors, mini charts and gallery markup without breaking URLs."""
from html import escape
import re


def migrate(path, original):
    if path.suffix != '.html':
        return original
    text = original.decode('utf-8')
    prefix = 'assets/' if path.name in {'index.html', 'index2.html', 'index3.html', 'index4.html'} else '../assets/'
    text = re.sub(r'<script\b[^>]*src="[^"\n]*jquery-migrate[^"\n]*"[^>]*></script>\s*\n?', '', text)
    text = text.replace('>Summernote</a>', '>Rich Text Editor</a>').replace('>Peity Chart</a>', '>Mini Charts</a>')
    if path.name in {'form-summernote.html', 'apps-compose-mail.html'}:
        text = re.sub(r'assets/plugins/summernote(?:-[\d.]+)?/summernote-bs5.min.css', 'assets/plugins/jodit-4.17.1/jodit.min.css', text)
        text = re.sub(r'assets/plugins/summernote(?:-[\d.]+)?/summernote-bs5.min.js', 'assets/plugins/jodit-4.17.1/jodit.min.js', text)
        text = text.replace('<!-- summernote -->', '<!-- Jodit rich text editor -->')
        text = text.replace('Form Summernote', 'Rich Text Editor')
        text = text.replace('<div id="summernote"></div>', '<textarea id="rich-text-editor" aria-label="Rich text editor"></textarea>')
        text = text.replace('Click on Edite button and change the text then save it.', 'Click Edit to change the text, then Save to keep it on this page.')
        text = text.replace('id="compose-textarea" class=', 'id="compose-textarea" aria-label="Message body" class=') if 'id="compose-textarea" aria-label=' not in text else text
    if path.name in {'chart-peity.html', 'index3.html'}:
        def chart(match):
            attrs, values = match.groups()
            kind = re.search(r'class="(pie|donut|bar|line)"', attrs)
            if not kind:
                return match[0]
            kind = {'donut': 'doughnut'}.get(kind[1], kind[1])
            attrs = re.sub(r'class="(?:pie|donut|bar|line)"', 'data-mini-chart="' + kind + '"', attrs)
            attrs = attrs.replace('data-peity=', 'data-chart-options=')
            return '<span' + attrs + ' data-values="' + escape(values, quote=True) + '">' + values + '</span>'
        text = re.sub(r'<span([^>]*)>([-\d.,/]+)</span>', chart, text)
        text = re.sub(r'<script src="[^"\n]*assets/plugins/peity/jquery.peity.min.js"></script>\s*', '', text)
        text = text.replace(prefix + 'plugins/functions/jquery.peity.init.js', prefix + 'js/mini-charts.js')
        if 'js/mini-charts.js' in text and 'chart-js-4.5.1/chart.umd.js' not in text:
            text = text.replace('<script src="' + prefix + 'js/mini-charts.js">', '<script src="' + prefix + 'plugins/chart-js-4.5.1/chart.umd.js"></script>\n<script src="' + prefix + 'js/mini-charts.js">')
        if 'css/mini-charts.css' not in text:
            text = text.replace('</head>', '<link rel="stylesheet" href="' + prefix + 'css/mini-charts.css">\n</head>')
        text = text.replace('Peity Charts', 'Mini Charts').replace('Peity Chart', 'Mini Charts').replace('Mini Chartss', 'Mini Charts')
        text = text.replace('<!-- Peity chart -->', '<!-- Chart.js mini charts -->').replace('<!-- Chart Peity JavaScript -->', '<!-- Chart.js mini charts -->')
        text = text.replace('Add code in span <code> class="pie"</code></code>', 'Use <code>data-mini-chart="pie"</code>')
        text = text.replace('Just add in span<code> class="donut"</code>', 'Use <code>data-mini-chart="doughnut"</code>')
        text = text.replace('Add class in span<code> peity-bar</code>', 'Use <code>data-mini-chart="bar"</code>')
        text = text.replace('Add class in span<code> peity-line</code>', 'Use <code>data-mini-chart="line"</code>')
    if path.name == 'pages-gallery.html':
        text = text.replace('../assets/plugins/cubeportfolio/css/cubeportfolio.min.css', '../assets/css/gallery.css')
        text = re.sub(r'<script src="[^"\n]*cubeportfolio/jquery.cubeportfolio.min.js"></script>\s*', '', text)
        text = text.replace('../assets/plugins/cubeportfolio/main.js', '../assets/js/gallery.js')
        text = re.sub(r'<!--[^>]*cubeportfolio[^>]*-->', '<!-- Native gallery -->', text)
        text = text.replace('id="js-filters-masonry"', 'id="gallery-filters"').replace('id="js-grid-masonry"', 'id="gallery-grid"')
        text = re.sub(r'<div data-filter="([^"]+)" class="cbp[^\"]+">\s*([^<]+)\s*<div class="cbp-filter-counter"></div>\s*</div>',
                      lambda m: '<button type="button" data-filter="' + m[1] + '" class="gallery-filter" aria-pressed="' + ('true' if m[1] == '*' else 'false') + '">' + m[2].strip() + ' <span class="gallery-counter"></span></button>', text)
        for old, new in {
            'cbp-l-filters-alignRight': 'gallery-filters', 'cbp-caption-defaultWrap': 'gallery-thumbnail',
            'cbp-caption-activeWrap': 'gallery-caption', 'cbp-l-caption-alignCenter': 'gallery-caption-content',
            'cbp-l-caption-body': 'gallery-caption-body', 'cbp-l-caption-title': 'gallery-title',
            'cbp-l-caption-desc': 'gallery-description', 'cbp-caption cbp-lightbox': 'gallery-link',
            'cbp-item': 'gallery-item', 'class="cbp"': 'class="gallery-grid"'
        }.items():
            text = text.replace(old, new)
        if 'id="gallery-lightbox"' not in text:
            text = text.replace('</body>', '''<dialog id="gallery-lightbox" class="gallery-lightbox" aria-label="Gallery image" aria-describedby="gallery-caption">
  <div class="gallery-lightbox-header">
    <span id="gallery-position" role="status" aria-live="polite"></span>
    <button type="button" class="btn btn-light border" data-gallery-close autofocus aria-label="Close image">Close</button>
  </div>
  <img alt="">
  <div class="gallery-lightbox-footer">
    <button type="button" class="btn btn-light border" data-gallery-prev aria-label="Previous image">Previous</button>
    <p id="gallery-caption"></p>
    <button type="button" class="btn btn-light border" data-gallery-next aria-label="Next image">Next</button>
  </div>
</dialog>
</body>''')
    text = re.sub(r'(<!-- (?:Native gallery|Jodit rich text editor|Chart.js mini charts) -->)[ \t]+(?=\n)', r'\1', text)
    text = re.sub(r'(<!-- Native gallery -->\n){2,}', '<!-- Native gallery -->\n', text)
    return text.encode('utf-8')
