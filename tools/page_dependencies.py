"""Keep page dependencies explicit; preserve jQuery for unknown integrations."""
from html.parser import HTMLParser
import re


class Scripts(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.sources = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'script' and attrs.get('src'):
            self.sources.append(attrs['src'].split('assets/')[-1])


NATIVE_SCRIPTS = {
    'bootstrap-components.js', 'chart-accessibility.js', 'chart-examples.js',
    'chart-theme.js', 'dashboard-charts.js', 'editable-tables.js', 'file-uploads.js',
    'gallery.js', 'grid-data.js', 'icon-catalog.js', 'icon-data.js', 'mini-charts.js',
    'niche.js', 'switches.js', 'text-editor.js',
}


def needs_jquery(text):
    for source in Scripts(text).sources:
        if source.startswith(('js/niche/', 'plugins/bootstrap-5.', 'plugins/popper-',
                              'plugins/chart-js-', 'plugins/chartjs/', 'plugins/jodit-',
                              'plugins/filepond-', 'plugins/filepond-plugin-', 'plugins/tabulator-')):
            continue
        if source.startswith('js/') and source[3:] in NATIVE_SCRIPTS:
            continue
        if re.match(r'plugins/jquery-[\d.]+/jquery\.min\.js$', source):
            continue
        return True
    return False


def prune(path, original):
    if path.suffix != '.html':
        return original
    text = original.decode('utf-8')
    # These examples use native/Bootstrap controls and never initialize jQuery UI.
    if path.name in {'apps-calendar.html', 'apps-contact-details.html', 'apps-contact-grid.html',
                     'apps-contacts.html', 'apps-support-ticket.html', 'pages-invoice.html', 'pages-profile.html'}:
        text = re.sub(r'^[ \t]*<script\b[^>]*src="[^"\n]*plugins/jquery-ui/[^"\n]*"[^>]*></script>[^\S\r\n]*\r?\n?', '', text, flags=re.M)
    if 'plugins/datatables-' not in ' '.join(Scripts(text).sources):
        text = re.sub(r'^[ \t]*<link\b[^>]*href="[^"\n]*plugins/datatables-[^"\n]*"[^>]*>[^\S\r\n]*\r?\n?', '', text, flags=re.M)
    if path.name == 'form-layouts.html':
        text = re.sub(r'^[ \t]*<link\b[^>]*href="[^"\n]*formwizard/jquery-steps.css"[^>]*>[^\S\r\n]*\r?\n?', '', text, flags=re.M)
    if path.name in {'ui-notification.html', 'ui-buttons.html', 'ui-grid.html', 'ui-progressbar.html'}:
        text = re.sub(r'^[ \t]*<link\b[^>]*href="[^"\n]*css/tabs.css"[^>]*>[^\S\r\n]*\r?\n?', '', text, flags=re.M)
    if not needs_jquery(text):
        text = re.sub(r'^[ \t]*<script\b[^>]*src="[^"\n]*(?:plugins/jquery-[\d.]+/jquery.min.js|js/niche/jquery-bridge.js)"[^>]*></script>[^\S\r\n]*\r?\n?', '', text, flags=re.M)
        text = re.sub(r'^[ \t]*<!-- jQuery 4 -->[^\S\r\n]*\r?\n?', '', text, flags=re.M)
    return text.encode('utf-8')
