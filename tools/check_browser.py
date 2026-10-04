#!/usr/bin/env python3
"""Check local pages and vendor integrations with Playwright's Chromium.

Optional tooling: pip install playwright && python -m playwright install chromium.
External services are blocked so the checks work independently of API keys/CDNs.
"""
import asyncio
import functools
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import threading

from playwright.async_api import async_playwright

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
            await page.close()

    pages = sorted(path.relative_to(ROOT) for path in ROOT.rglob('*.html'))
    await asyncio.gather(*(check_page(path) for path in pages))
    assert not failures, '\n'.join(failures)
    print(f'PASS: {len(pages)} pages load with jQuery 4, no JavaScript errors or missing local resources.', flush=True)

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
    await page.locator('.note-editable').first.fill('Editor integration test')
    assert 'Editor integration test' in await page.evaluate("jQuery('#summernote').summernote('code')")
    await page.click('#edit')
    assert await page.locator('.note-editable').count() == 2
    await page.click('#save')
    assert await page.locator('.note-editable').count() == 1
    print('PASS: Summernote initializes after Bootstrap, accepts text and switches the editable demo between edit/save.', flush=True)

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
                           ('ui/ui-range-slider.html', '.irs')]:
        await visit(path)
        assert await page.locator(selector).first.is_visible(), path
    assert not failures, '\n'.join(failures)
    print('PASS: upgraded widgets also render at a mobile viewport.', flush=True)
    await context.close()


async def main():
    server = ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(QuietHandler, directory=str(ROOT)))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    try:
        async with async_playwright() as playwright:
            browser = await playwright.chromium.launch()
            try:
                await check(browser, f'http://127.0.0.1:{server.server_port}')
            finally:
                await browser.close()
    finally:
        server.shutdown()
        server.server_close()


if __name__ == '__main__':
    asyncio.run(main())
