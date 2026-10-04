#!/usr/bin/env python3
"""Check local pages and vendor integrations with Playwright's Chromium.

Optional tooling: pip install -r tools/requirements-test.txt
and python -m playwright install chromium.
External services are blocked so the checks work independently of API keys/CDNs.
"""
import asyncio
import functools
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import threading

from playwright.async_api import async_playwright
from check_native_components import check_native
from check_design_quality import check_design

ROOT = Path(__file__).resolve().parents[1]


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


async def check(browser, base_url):
    context = await browser.new_context(viewport={'width': 1440, 'height': 1000})
    await context.route('**/*', lambda route: route.continue_()
                        if route.request.url.startswith((base_url, 'blob:', 'data:'))
                        else route.abort())
    failures = []
    semaphore = asyncio.Semaphore(4)

    async def check_page(path):
        async with semaphore:
            page = await context.new_page()
            page.on('pageerror', lambda error: failures.append(str(path) + ': ' + str(error)))
            page.on('response', lambda response: failures.append(response.url + ': ' + str(response.status))
                    if response.status >= 400 and response.url.startswith(base_url) else None)
            await page.goto(base_url + '/' + path.as_posix(), wait_until='load')
            await page.wait_for_timeout(600)
            assert await page.evaluate('jQuery.fn.jquery') == '4.0.0', str(path)
            assert await page.evaluate("typeof jQuery.migrateVersion === 'undefined'"), str(path)
            await page.evaluate('document.fonts.ready')
            assert await page.evaluate("document.fonts.check('400 16px Poppins')"), str(path)
            await page.add_script_tag(path=str(ROOT / 'tools/test-vendor/axe-core-4.13.0/axe.min.js'))
            violations = await page.evaluate("""axe.run(document, {runOnly: {type: 'rule', values:
                ['color-contrast', 'image-alt', 'button-name', 'link-name', 'label', 'meta-viewport',
                 'aria-valid-attr-value', 'aria-valid-attr', 'duplicate-id-aria']}})
                .then(result => result.violations.map(v => ({rule: v.id, elements: v.nodes.map(n => n.target)})))""")
            assert not violations, f'{path}: {violations}'
            await page.close()

    pages = sorted(path.relative_to(ROOT) for path in ROOT.rglob('*.html'))
    await asyncio.gather(*(check_page(path) for path in pages))
    assert not failures, '\n'.join(failures)
    print(f'PASS: {len(pages)} pages load with jQuery 4, no JavaScript errors or missing local resources.', flush=True)
    print('PASS: local Poppins loads and axe checks text contrast, image alternatives, control names, form labels, zoom and valid ARIA on every page.', flush=True)

    # Record instances inside the test browser without exposing application globals.
    async def record_calendars(route):
        response = await route.fetch()
        await route.fulfill(response=response, body=await response.text() + '''
window.testCalendars = [];
FullCalendar.Calendar = class extends FullCalendar.Calendar {
    constructor(...args) { super(...args); window.testCalendars.push(this); }
};''')

    await context.route('**/fullcalendar-7.1.0/js/fullcalendar.min.js', record_calendars)
    page = await context.new_page()
    page.on('pageerror', lambda error: failures.append(str(error)))

    async def visit(path):
        await page.goto(base_url + '/' + path, wait_until='load')
        await page.wait_for_timeout(600)

    await visit('index.html')
    await page.keyboard.press('Tab')
    assert await page.locator('.niche-skip-link').evaluate('el => el === document.activeElement')
    await page.keyboard.press('Enter')
    assert await page.evaluate("document.activeElement.id === 'main-content'")
    branch = page.locator('#respMenu > li > a').first
    await branch.focus()
    assert await branch.get_attribute('aria-expanded') == 'true'
    await branch.press('ArrowDown')
    assert await page.evaluate("document.activeElement.closest('ul.sub-menu') !== null")
    await page.keyboard.press('Escape')
    assert await branch.evaluate('el => el === document.activeElement')
    assert await branch.get_attribute('aria-expanded') == 'false'
    assert await page.evaluate("['line-chart', 'pie-chart', 'area-chart'].every(id => Chart.getChart(id))")
    assert await page.evaluate("Chart.defaults.font.family === getComputedStyle(document.body).fontFamily")
    assert await page.locator('.info-box .list-inline').count() == 0
    await page.locator('#line-chart').scroll_into_view_if_needed()
    chart_legend = await page.evaluate('''() => {
        const chart = Chart.getChart('line-chart');
        const box = chart.legend.legendHitBoxes[0];
        const bounds = chart.canvas.getBoundingClientRect();
        return {x: bounds.x + box.left + box.width / 2, y: bounds.y + box.top + box.height / 2};
    }''')
    await page.mouse.click(chart_legend['x'], chart_legend['y'])
    await page.wait_for_function("!Chart.getChart('line-chart').isDatasetVisible(0)")
    await page.mouse.click(chart_legend['x'], chart_legend['y'])
    await page.wait_for_function("Chart.getChart('line-chart').isDatasetVisible(0)")
    assert await page.evaluate("typeof jQuery.fn.layout.Constructor === 'function' && !!jQuery('body').data('lte.layout')")
    assert await page.evaluate("document.getElementById('respMenu').dataset.nicheMenuInitialized === 'true'")
    await page.set_viewport_size({'width': 390, 'height': 844})
    await page.wait_for_timeout(300)
    await page.click('#menu-btn')
    await page.wait_for_function("!document.getElementById('respMenu').classList.contains('hide-menu')")
    assert await page.locator('#menu-btn').get_attribute('aria-expanded') == 'true'
    await page.click('#menu-btn')
    await page.wait_for_function("document.getElementById('respMenu').classList.contains('hide-menu')")
    assert await page.locator('#menu-btn').get_attribute('aria-expanded') == 'false'
    await page.set_viewport_size({'width': 1440, 'height': 1000})
    print('PASS: shared navigation initializes once, mobile menu toggles and three dashboard charts render.', flush=True)

    await visit('apps/apps-mailbox.html')
    box = page.locator('.box').first
    await page.evaluate("jQuery('.box').boxWidget()")  # Reusing the plugin must not bind click handlers again.
    await box.locator('[data-widget=collapse]').click()
    await page.wait_for_function("document.querySelector('.box').classList.contains('collapsed-box')")
    assert await box.locator('[data-widget=collapse]').get_attribute('aria-expanded') == 'false'
    await box.locator('[data-widget=collapse]').click()
    await page.wait_for_function("!document.querySelector('.box').classList.contains('collapsed-box')")
    await box.locator('.box-body').wait_for(state='visible')
    assert await box.locator('[data-widget=collapse]').get_attribute('aria-expanded') == 'true'
    await visit('tables/table-data-table.html')
    assert await page.evaluate('DataTable.isDataTable(document.getElementById("example1"))')
    print('PASS: shared DataTables initializes and box widgets collapse/expand without duplicate handlers.', flush=True)

    # Exercise retained plugin APIs whose components are optional in this horizontal template.
    assert await page.evaluate('''() => {
        const fixture = document.createElement('div');
        fixture.innerHTML = '<ul id="test-tree"><li class="treeview"><a href="#">Parent</a><ul class="treeview-menu" style="display:none"><li>Child</li></ul></li></ul>'
            + '<ul id="test-todo"><li><input type="checkbox"></li></ul>'
            + '<div class="direct-chat"><button data-widget="chat-pane-toggle">Chat</button></div>'
            + '<button data-toggle="push-menu">Sidebar</button><button data-toggle="control-sidebar">Settings</button><aside class="control-sidebar"></aside>';
        document.body.appendChild(fixture);
        const $ = jQuery;
        $('#test-tree').tree({animationSpeed: 0});
        $('#test-tree > li > a').trigger('click');
        const opened = $('#test-tree > li').hasClass('menu-open');
        $('#test-tree > li > a').trigger('click');
        const treeClosed = !$('#test-tree > li').hasClass('menu-open');
        $('#test-todo').todoList();
        const checkbox = $('#test-todo input');
        checkbox.prop('checked', true).trigger('change');
        const done = checkbox.closest('li').hasClass('done');
        checkbox.prop('checked', false).trigger('change');
        const unchecked = !checkbox.closest('li').hasClass('done');
        const customTodo = document.createElement('ul');
        customTodo.innerHTML = '<li><input type="checkbox"></li>';
        fixture.append(customTodo);
        let callbacks = 0;
        $(customTodo).data('onCheck', function () { if (this.jquery === $.fn.jquery) callbacks++; }).todoList();
        $('input', customTodo).prop('checked', true).trigger('change');
        const compatibleCallbacks = callbacks === 1;
        const legacyTodo = $.fn.todoList.noConflict();
        const noConflict = $.fn.todoList === undefined;
        $.fn.todoList = legacyTodo;
        $('.direct-chat button', fixture).trigger('click');
        const chat = $('.direct-chat', fixture).hasClass('direct-chat-contacts-open');
        $('[data-toggle="push-menu"]', fixture).trigger('click');
        const collapsed = $('body').hasClass('sidebar-collapse');
        $('[data-toggle="push-menu"]', fixture).trigger('click');
        $('[data-toggle="control-sidebar"]', fixture).trigger('click');
        const settings = $('.control-sidebar', fixture).hasClass('control-sidebar-open');
        $('[data-toggle="control-sidebar"]', fixture).trigger('click');
        const closed = !$('.control-sidebar', fixture).hasClass('control-sidebar-open');
        fixture.remove();
        return opened && treeClosed && done && unchecked && compatibleCallbacks && noConflict && chat && collapsed && settings && closed;
    }''')
    print('PASS: retained tree, todo, chat and sidebar plugin APIs work with delegated events.', flush=True)

    await visit('forms/form-wizard.html')
    await page.locator('#demo1 [data-direction=next]').click()
    await page.locator('#frmRes').wait_for(state='visible')
    assert await page.locator('#frmRes .invalid-feedback:visible').count() == 4
    assert await page.locator('#frmRes [name=firstname]').evaluate('el => el === document.activeElement')
    assert await page.locator('#frmRes [name=firstname]').evaluate('''el =>
        el.getAttribute('aria-describedby').split(' ').some(id => document.getElementById(id).textContent.includes('first name'))''')
    await page.add_script_tag(path=str(ROOT / 'tools/test-vendor/axe-core-4.13.0/axe.min.js'))
    assert await page.evaluate("axe.run(document.querySelector('#frmRes'), {runOnly: ['color-contrast', 'aria-valid-attr-value', 'label']}).then(result => result.violations.length)") == 0
    await page.locator('#frmRes [name=email]').fill('invalid-email')
    await page.locator('#demo1 [data-direction=next]').click()
    assert await page.locator('#frmRes .invalid-feedback:visible').filter(has_text='Enter a valid email address').count() == 1
    for field, value in {'firstname': 'Example', 'lastname': 'User', 'email': 'tester@example.com', 'phoneno': '5551234'}.items():
        await page.locator('#frmRes [name=' + field + ']').fill(value)
    await page.locator('#frmRes [name=phoneno]').press('Tab')
    await page.locator('#demo1 [data-direction=next]').click()
    await page.locator('#frmInfo').wait_for(state='visible')
    await page.locator('#demo1 [data-direction=next]').click()
    assert await page.locator('#frmInfo .is-invalid').count() > 0
    await page.locator('#demo1 [data-direction=prev]').click()
    await page.locator('#frmRes').wait_for(state='visible')
    assert await page.locator('#frmInfo .is-invalid').count() == 0
    assert await page.locator('#frmRes .invalid-feedback:visible').count() == 0
    print('PASS: extracted wizard blocks invalid steps, advances with required fields and returns to previous steps.', flush=True)

    await visit('apps/apps-calendar.html')
    assert await page.evaluate('testCalendars.length') == 2
    assert await page.evaluate('testCalendars.every(c => c.getEvents().length === 6)')
    assert await page.evaluate("testCalendars.every(c => c.getEvents().find(e => e.title === 'All Day Event').allDay)")
    await page.fill('#new-event', 'Calendar integration test')
    await page.click('#add-new-event')
    await page.check('#drop-remove')
    source = page.locator('#external-events .external-event').first
    target = page.locator('#calendar [role=gridcell][data-date]').nth(10)
    start, end = await source.bounding_box(), await target.bounding_box()
    await page.mouse.move(start['x'] + start['width'] / 2, start['y'] + start['height'] / 2)
    await page.mouse.down()
    await page.mouse.move(end['x'] + end['width'] / 2, end['y'] + end['height'] / 2, steps=20)
    await page.wait_for_timeout(200)
    await page.mouse.up()
    await page.wait_for_function("testCalendars[0].getEvents().some(e => e.title === 'Calendar integration test')")
    assert await page.locator('#external-events').get_by_text('Calendar integration test', exact=True).count() == 0
    await page.locator('#calendar button[role=tab]').filter(has_text='Week').click()
    await page.wait_for_function("testCalendars[0].view.type === 'timeGridWeek'")
    await page.locator('#calendar button[role=tab]').filter(has_text='Day').click()
    await page.wait_for_function("testCalendars[0].view.type === 'timeGridDay'")
    print('PASS: FullCalendar renders events, receives a real drag, removes its source and changes views.', flush=True)

    await visit('ui/ui-range-slider.html')
    assert await page.locator('.irs--modern').count() == 7
    assert await page.evaluate("jQuery('#range_02').data('ionRangeSlider').result.from") == 550
    await page.evaluate("jQuery('#range_03').data('ionRangeSlider').update({from: 300, to: 700})")
    assert await page.evaluate("document.getElementById('range_03').value") == '300;700'
    print('PASS: seven Ion.RangeSlider widgets render and update their range values.', flush=True)

    await visit('forms/form-uploads.html')
    assert await page.locator('.filepond--root').count() == 8
    assert await page.evaluate("[...document.querySelectorAll('.filepond--root')].filter(el => FilePond.find(el).disabled).length") == 2
    assert await page.evaluate("[...document.querySelectorAll('.filepond--root')].flatMap(el => FilePond.find(el).getFiles()).length") == 3
    assert await page.evaluate('''async () => {
        const pond = FilePond.find(document.querySelector('.filepond--root'));
        const file = await pond.addFile(new File(['sample'], 'sample.txt'));
        return file.filename;
    }''') == 'sample.txt'
    assert await page.evaluate('''async () => {
        const pond = [...document.querySelectorAll('.filepond--root')].map(el => FilePond.find(el)).find(p => p.maxFileSize);
        try { await pond.addFile(new File([new Uint8Array(3 * 1024 * 1024)], 'large.bin')); return false; }
        catch (error) { return error.error.main === 'File is too large'; }
    }''')
    await visit('apps/apps-compose-mail.html')
    assert await page.evaluate('''async () => {
        const pond = FilePond.find(document.querySelector('.filepond--root'));
        await pond.addFiles([new File(['a'], 'a.txt'), new File(['b'], 'b.txt')]);
        return pond.allowMultiple && pond.getFiles().length === 2;
    }''')
    print('PASS: FilePond loads previews, preserves disabled inputs, rejects oversized files and accepts multiple attachments.', flush=True)

    await visit('tables/table-jsgrid.html')
    assert await page.evaluate("['#basicscenario', '#staticdata', '#soarting'].every(s => Tabulator.findTable(s)[0].getDataCount() === 100)")
    await page.evaluate("Tabulator.findTable('#basicscenario')[0].getRows()[0].getCell('Name').edit()")
    editor = page.locator('#basicscenario .tabulator-editing input')
    await editor.fill('Edited client')
    await editor.press('Enter')
    assert await page.evaluate("Tabulator.findTable('#basicscenario')[0].getRows()[0].getData().Name") == 'Edited client'
    assert await page.evaluate("Tabulator.findTable('#staticdata')[0].getRows()[0].getData().Name") == 'Otto Clay'
    await page.evaluate("Tabulator.findTable('#basicscenario')[0].setHeaderFilterValue('Name', 'Edited client')")
    await page.wait_for_function("Tabulator.findTable('#basicscenario')[0].getDataCount('active') === 1")
    page.once('dialog', lambda dialog: dialog.accept())
    await page.locator('#basicscenario').get_by_role('button', name='Delete', exact=True).click()
    await page.wait_for_function("Tabulator.findTable('#basicscenario')[0].getDataCount() === 99")
    await page.select_option('#sortingField', 'Age')
    await page.wait_for_function("Tabulator.findTable('#soarting')[0].getSorters()[0].field === 'Age'")
    print('PASS: Tabulator edits, isolates demo data, filters, confirms deletion and applies the external sort selector.', flush=True)

    await visit('forms/form-summernote.html')
    await page.locator('.jodit-wysiwyg').first.fill('Editor integration test')
    await page.locator('.jodit-wysiwyg').first.press('Control+a')
    await page.locator('.jodit-toolbar-button_bold button').click()
    await page.wait_for_function("/<(strong|b)>Editor integration test/.test(Jodit.instances['rich-text-editor'].value)")
    await page.locator('.jodit-toolbar-button_source button').click()
    await page.locator('.jodit-source__mirror').fill('<p><em>HTML editing</em></p><table><tbody><tr><td>Table cell</td></tr></tbody></table>')
    await page.locator('.jodit-toolbar-button_source button').click()
    assert await page.locator('.jodit-wysiwyg table td').inner_text() == 'Table cell'
    assert await page.locator('.jodit-wysiwyg em').inner_text() == 'HTML editing'
    await page.locator('.jodit-toolbar-button_image button').click()
    await page.locator('.jodit-popup input[type=file]').set_input_files(ROOT / 'assets/img/img1.jpg')
    await page.wait_for_function("Jodit.instances['rich-text-editor'].value.includes('data:image/jpeg;base64,')")
    await page.locator('.jodit-toolbar-button_fullsize button').click()
    await page.wait_for_function("document.querySelector('.jodit-container').classList.contains('jodit_fullsize')")
    await page.locator('.jodit-toolbar-button_fullsize button').click()
    await page.click('#edit')
    assert await page.locator('.jodit-wysiwyg').count() == 2
    await page.click('#edit')  # Repeated Edit must not add another toolbar/instance.
    assert await page.locator('.jodit-wysiwyg').count() == 2
    await page.locator('.jodit-wysiwyg').last.fill('Saved edited content')
    await page.click('#save')
    assert await page.locator('.jodit-wysiwyg').count() == 1
    assert await page.locator('.click2edit').inner_text() == 'Saved edited content'
    await page.click('#edit')
    assert await page.locator('.jodit-wysiwyg').last.inner_text() == 'Saved edited content'
    await page.click('#save')
    await visit('apps/apps-compose-mail.html')
    await page.locator('.jodit-wysiwyg').fill('Message body test')
    await page.wait_for_function("document.getElementById('compose-textarea').value.includes('Message body test')")
    print('PASS: Jodit formats text, edits HTML/tables, embeds local images, toggles fullscreen and preserves edit/save and message content.', flush=True)

    await visit('charts/chart-peity.html')
    assert await page.locator('[data-mini-chart] canvas').count() == 18
    assert await page.evaluate("[...document.querySelectorAll('[data-mini-chart] canvas')].every(el => Chart.getChart(el))")
    assert await page.evaluate("Chart.getChart(document.querySelector('[data-mini-chart=pie] canvas')).data.datasets[0].data.join(',')") == '1,4'
    assert await page.evaluate("[...document.querySelectorAll('[data-mini-chart=bar] canvas')].some(el => Chart.getChart(el).data.datasets[0].data.includes(-7))")
    await visit('index3.html')
    assert await page.locator('[data-mini-chart] canvas').count() == 3
    assert await page.evaluate("Chart.getChart(document.querySelector('[data-mini-chart] canvas')).data.datasets[0].backgroundColor[0]") == '#f96262'
    print('PASS: 18 mini charts and three dashboard charts preserve ratios, negative series and custom colors.', flush=True)

    await visit('pages/pages-gallery.html')
    assert await page.locator('.gallery-item:visible').count() == 12
    for selector in ('.identity', '.web-design', '.graphic', '.graphic, .identity', '*'):
        button = page.locator('.gallery-filter[data-filter="' + selector + '"]')
        expected = await page.evaluate("selector => [...document.querySelectorAll('.gallery-item')].filter(el => selector === '*' || el.matches(selector)).length", selector)
        await button.click()
        assert await page.locator('.gallery-item:visible').count() == expected
        assert await button.get_attribute('aria-pressed') == 'true'
        assert '(' + str(expected) + ')' in await button.inner_text()
    await page.locator('.gallery-filter[data-filter=".identity"]').click()
    await page.locator('.gallery-item:visible .gallery-link').first.click()
    await page.wait_for_function("document.getElementById('gallery-lightbox').open")
    await page.wait_for_function("document.querySelector('#gallery-lightbox img').complete && document.querySelector('#gallery-lightbox img').naturalWidth > 0")
    first_image = await page.locator('#gallery-lightbox img').get_attribute('src')
    assert await page.locator('#gallery-position').inner_text() == '1 of 5'
    await page.locator('[data-gallery-next]').click()
    assert await page.locator('#gallery-lightbox img').get_attribute('src') != first_image
    await page.keyboard.press('ArrowLeft')
    assert await page.locator('#gallery-lightbox img').get_attribute('src') == first_image
    await page.locator('[data-gallery-prev]').click()
    assert await page.locator('#gallery-position').inner_text() == '5 of 5'
    await page.keyboard.press('Escape')
    assert not await page.locator('#gallery-lightbox').is_visible()
    assert await page.locator('.gallery-item:visible .gallery-link').first.evaluate('el => el === document.activeElement')
    await page.locator('.gallery-item:visible .gallery-link').first.click()
    await page.locator('[data-gallery-close]').click()
    assert not await page.locator('#gallery-lightbox').is_visible()
    print('PASS: native gallery filters/counts categories, navigates the filtered lightbox and restores focus on close.', flush=True)

    await visit('icons/icon-fontawesome.html')
    initial_count = await page.locator('#icon-catalog > div').count()
    await page.fill('#icon-search', 'calendar')
    assert 0 < await page.locator('#icon-catalog > div').count() < initial_count
    await page.evaluate('document.fonts.ready')
    assert await page.evaluate("document.fonts.check('16px bootstrap-icons')")
    assert await page.evaluate("[...document.querySelectorAll('#icon-catalog > div')].every(el => el.textContent.includes('calendar'))")
    print('PASS: Bootstrap Icons loads its local font and searches the generated catalog.', flush=True)

    await page.set_viewport_size({'width': 390, 'height': 844})
    for path, selector in [('apps/apps-calendar.html', '#calendar [role=grid]'),
                           ('forms/form-uploads.html', '.filepond--root'),
                           ('tables/table-jsgrid.html', '.tabulator'),
                           ('ui/ui-range-slider.html', '.irs'),
                           ('forms/form-summernote.html', '.jodit-wysiwyg'),
                           ('pages/pages-gallery.html', '.gallery-item'),
                           ('charts/chart-peity.html', '[data-mini-chart] canvas')]:
        await visit(path)
        assert await page.locator(selector).first.is_visible(), path
        if path == 'pages/pages-gallery.html':
            assert await page.locator('#gallery-grid').evaluate("el => getComputedStyle(el).gridTemplateColumns.split(' ').length") == 1
    for path in ('ui/ui-tab.html', 'forms/form-wizard.html', 'index.html'):
        await visit(path)
        await page.add_script_tag(path=str(ROOT / 'tools/test-vendor/axe-core-4.13.0/axe.min.js'))
        violations = await page.evaluate("""axe.run(document, {runOnly: {type: 'rule', values:
            ['color-contrast', 'image-alt', 'button-name', 'link-name', 'label', 'meta-viewport',
             'aria-valid-attr-value', 'aria-valid-attr', 'duplicate-id-aria']}})
            .then(result => result.violations.map(v => v.id))""")
        assert not violations, f'Mobile {path}: {violations}'
    assert not failures, '\n'.join(failures)
    print('PASS: upgraded widgets also render at a mobile viewport.', flush=True)
    await check_design(page, visit)
    await context.close()


async def main():
    server = ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(QuietHandler, directory=str(ROOT)))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    try:
        async with async_playwright() as playwright:
            browser = await playwright.chromium.launch()
            try:
                await check_native(browser, f'http://127.0.0.1:{server.server_port}')
                await check(browser, f'http://127.0.0.1:{server.server_port}')
            finally:
                await browser.close()
    finally:
        server.shutdown()
        server.server_close()


if __name__ == '__main__':
    asyncio.run(main())
