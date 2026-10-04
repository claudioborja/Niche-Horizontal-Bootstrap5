"""Make standalone examples explicit without changing functional controls."""
import re

AUTH_PAGES = {'pages-login.html', 'pages-login-2.html', 'pages-register.html',
              'pages-register2.html', 'pages-recover-password.html', 'pages-lockscreen.html'}


def migrate(path, original):
    if path.suffix != '.html':
        return original
    text = original.decode('utf-8')
    prefix = 'assets/' if path.name in {'index.html', 'index2.html', 'index3.html', 'index4.html'} else '../assets/'
    home = 'index.html' if prefix == 'assets/' else '../index.html'
    text = re.sub(r'(<a\b[^>]*?)href="#"([^>]*>\s*(?:<i\b[^>]*></i>\s*)?Home\s*</a>)',
                  lambda match: match[1] + 'href="' + home + '"' + match[2], text)
    if path.name in AUTH_PAGES:
        def local_form(match):
            tag = re.sub(r'\s+(?:action|method)="[^"]*"', '', match[0])
            return tag if 'data-demo-form' in tag else tag.replace('<form', '<form data-demo-form="true"', 1)
        text = re.sub(r'<form\b[^>]*>', local_form, text)
    if path.name == 'apps-compose-mail.html':
        text = text.replace('<button type="submit" class="btn btn-primary"><i class="fa fa-envelope-o"',
                            '<button type="button" data-demo-action="true" data-demo-message="Demo message. No email was sent." class="btn btn-primary"><i class="fa fa-envelope-o"')
        text = text.replace('<button type="button" class="btn btn-light border"><i class="fa fa-pencil"',
                            '<button type="button" data-demo-action="true" data-demo-message="Demo draft. The message stays on this page and is not saved." class="btn btn-light border"><i class="fa fa-pencil"')
    if 'assets/js/demo-actions.js' not in text:
        text = text.replace('</body>', '<script src="' + prefix + 'js/demo-actions.js"></script>\n</body>')
    return text.encode('utf-8')
