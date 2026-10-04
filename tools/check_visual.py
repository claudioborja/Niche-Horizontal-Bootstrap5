#!/usr/bin/env python3
"""Compare deterministic Chromium screenshots; baseline updates are explicit."""
import argparse
import asyncio
from datetime import datetime, timezone
import functools
from http.server import ThreadingHTTPServer
from importlib.metadata import version
import json
from pathlib import Path
import shutil
import sys
import threading

from PIL import Image, ImageChops
from playwright.async_api import async_playwright
from check_browser import QuietHandler

ROOT = Path(__file__).resolve().parents[1]
BASELINES = ROOT / 'tools/visual-baselines'
CASES = (
    ('dashboard', 'index.html', ''),
    ('charts', 'index4.html', 'chart-data'),
    ('calendar', 'apps/apps-calendar.html', ''),
    ('validation', 'forms/form-validation.html', ''),
    ('wizard-errors', 'forms/form-wizard.html', 'wizard-errors'),
    ('data-table', 'tables/table-data-table.html', ''),
    ('gallery', 'pages/pages-gallery.html', ''),
    ('login', 'pages/pages-login.html', ''),
    ('demo-notice', 'index.html', 'demo-notice'),
    ('navigation-open', 'index.html', 'navigation-open'),
    ('account-open', 'index.html', 'account-open'),
    ('gallery-filtered', 'pages/pages-gallery.html', 'gallery-filtered'),
    ('gallery-dialog', 'pages/pages-gallery.html', 'gallery-dialog'),
    ('tabs-profile', 'ui/ui-tab.html', 'tabs-profile'),
    ('tabs-vertical', 'ui/ui-tab.html', 'tabs-vertical'),
    ('table-filtered', 'tables/table-data-table.html', 'table-filtered'),
    ('table-empty', 'tables/table-data-table.html', 'table-empty'),
    ('mailbox-collapsed', 'apps/apps-mailbox.html', 'mailbox-collapsed'),
    ('popover-open', 'ui/ui-tooltip-popover.html', 'popover-open'),
    ('faq-expanded', 'pages/pages-faq.html', 'faq-expanded'),
)
OVERLAYS = {'navigation-open', 'account-open', 'gallery-dialog', 'popover-open'}


async def interactive_state(page, state, width):
    """Use real controls and verify their state before accepting a screenshot."""
    if state == 'navigation-open':
        if width < 768:
            await page.locator('#menu-btn').click()
            assert await page.locator('#menu-btn').get_attribute('aria-expanded') == 'true'
        branch = page.locator('#respMenu > li > a').first
        await branch.focus()
        await branch.press('ArrowDown')
        assert await branch.get_attribute('aria-expanded') == 'true'
        await page.locator('#' + await branch.get_attribute('aria-controls')).wait_for(state='visible')
    elif state == 'account-open':
        await page.locator('.user-menu > a').click()
        await page.locator('.user-menu > .dropdown-menu').wait_for(state='visible')
        assert await page.locator('.user-menu > a').get_attribute('aria-expanded') == 'true'
    elif state in {'gallery-filtered', 'gallery-dialog'}:
        await page.locator('.gallery-filter[data-filter=".identity"]').click()
        assert await page.locator('.gallery-item:visible').count() == 5
        if state == 'gallery-dialog':
            await page.locator('.gallery-item:visible .gallery-link').first.click()
            await page.locator('#gallery-lightbox').wait_for(state='visible')
            assert await page.locator('#gallery-lightbox').evaluate('el => el.open')
            await page.locator('#gallery-lightbox img').evaluate('image => image.decode()')
            assert await page.locator('#gallery-position').inner_text() == '1 of 5'
    elif state in {'tabs-profile', 'tabs-vertical'}:
        suffix = '' if state == 'tabs-profile' else '9'
        tab = page.locator('#profile' + suffix + '-tab')
        await tab.click()
        await page.locator('#profile' + suffix).wait_for(state='visible')
        assert await tab.get_attribute('aria-selected') == 'true'
    elif state in {'table-filtered', 'table-empty'}:
        query = 'Trident' if state == 'table-filtered' else 'No matching visual fixture'
        await page.locator('#example1_wrapper .dt-search input').fill(query)
        if state == 'table-filtered':
            await page.wait_for_function("0 < new DataTable('#example1').rows({search: 'applied'}).count() && new DataTable('#example1').rows({search: 'applied'}).count() < new DataTable('#example1').rows().count()")
            assert await page.locator('#example1 tbody tr').first.inner_text() != ''
        else:
            await page.wait_for_function("new DataTable('#example1').rows({search: 'applied'}).count() === 0")
            assert 'No matching records found' in await page.locator('#example1 tbody').inner_text()
    elif state == 'mailbox-collapsed':
        box = page.locator('.box').first
        control = box.locator('[data-widget=collapse]')
        await control.click()
        await page.wait_for_function("document.querySelector('.box').classList.contains('collapsed-box')")
        assert await control.get_attribute('aria-expanded') == 'false'
    elif state == 'popover-open':
        await page.locator('[data-popover-template="myPopover1"]').click()
        await page.locator('.popover.show').wait_for(state='visible')
        assert await page.locator('.popover.show [data-popover-close]').is_visible()
    elif state == 'faq-expanded':
        await page.locator('[data-bs-target="#collapseTwo"]').click()
        await page.locator('#collapseTwo.show').wait_for(state='visible')
        assert await page.locator('[data-bs-target="#collapseTwo"]').get_attribute('aria-expanded') == 'true'
        assert not await page.locator('#collapseOne').is_visible()
    else:
        raise ValueError('Unknown interactive visual state: ' + state)
    if state and state not in OVERLAYS:
        await page.evaluate('window.scrollTo(0, 0)')
    await page.evaluate('new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)))')


def compare(expected, actual, threshold=12):
    with Image.open(expected) as source, Image.open(actual) as target:
        left, right = source.convert('RGB'), target.convert('RGB')
        if left.size != right.size:
            return 1.0, None
        bands = ImageChops.difference(left, right).split()
        maximum = ImageChops.lighter(ImageChops.lighter(bands[0], bands[1]), bands[2])
        mask = maximum.point(lambda value: 255 if value > threshold else 0)
        ratio = mask.histogram()[255] / (left.width * left.height)
        highlighted = right.copy()
        highlighted.paste((255, 0, 100), mask=mask)
        return ratio, highlighted


async def capture(browser, base_url, output):
    context = await browser.new_context(locale='en-US', timezone_id='UTC',
                                        color_scheme='light', reduced_motion='reduce', device_scale_factor=1)
    await context.route('**/*', lambda route: route.continue_()
                        if route.request.url.startswith((base_url, 'data:', 'blob:')) else route.abort())
    results = []
    for width, height in ((1440, 1000), (390, 844)):
        for name, path, state in CASES:
            page = await context.new_page()
            await page.set_viewport_size({'width': width, 'height': height})
            errors = []
            page.on('pageerror', lambda error: errors.append(str(error)))
            # Only Date is fixed; normal timers remain available to the widgets.
            await page.clock.set_fixed_time(datetime(2026, 1, 15, 12, tzinfo=timezone.utc))
            await page.goto(base_url + '/' + path, wait_until='load')
            await page.evaluate('document.fonts.ready')
            await page.wait_for_timeout(600)
            if state == 'wizard-errors':
                await page.locator('#demo1 [data-direction=next]').click()
                await page.locator('#frmRes .invalid-feedback').first.wait_for(state='visible')
            elif state == 'chart-data':
                await page.locator('.chart-data summary').first.click()
            elif state == 'demo-notice':
                await page.locator('.main-footer [data-demo-action]').first.click()
                await page.locator('.demo-status').wait_for(state='visible')
            # Trigger all lazy images, then return to a consistent scroll position.
            await page.evaluate("document.querySelectorAll('img[loading=lazy]').forEach(image => image.loading = 'eager')")
            await page.evaluate("Promise.all([...document.images].map(image => image.decode().catch(() => {})))")
            await page.evaluate('window.scrollTo(0, 0)')
            await page.wait_for_timeout(100)
            await page.evaluate("""() => {
                if (window.Chart) Object.values(Chart.instances).forEach(chart => {
                    chart.resize();
                    chart.update('none');
                });
                return new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)));
            }""")
            if state not in {'', 'wizard-errors', 'chart-data', 'demo-notice'}:
                await interactive_state(page, state, width)
            assert not errors, f'{path}: {errors}'
            filename = f'{name}-{width}.png'
            await page.screenshot(path=str(output / filename), full_page=state not in OVERLAYS, animations='disabled', caret='hide')
            results.append(filename)
            await page.close()
    await context.close()
    return results


async def run(args, base_url):
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch()
        try:
            environment = {'browser': browser.version, 'playwright': version('playwright'), 'platform': sys.platform}
            manifest = BASELINES / 'manifest.json'
            if not args.update:
                if not manifest.is_file():
                    raise SystemExit('Missing baselines. Create them with --update after reviewing the design.')
                expected = json.loads(manifest.read_text())
                if expected['environment'] != environment:
                    raise SystemExit('Visual baseline environment differs. Use the pinned Linux Chromium/Python tooling.')
            files = await capture(browser, base_url, output)
        finally:
            await browser.close()
    if args.update:
        BASELINES.mkdir(parents=True, exist_ok=True)
        for filename in files:
            shutil.copyfile(output / filename, BASELINES / filename)
        manifest.write_text(json.dumps({'environment': environment, 'files': files}, indent=2) + '\n')
        print(f'Created {len(files)} baselines. Review the images before committing them.')
        return
    assert files == expected['files'], 'Visual case list changed; review and update the baselines explicitly.'
    report = []
    for filename in files:
        baseline = BASELINES / filename
        if not baseline.is_file():
            raise SystemExit('Missing visual baseline: ' + filename)
        ratio, diff = compare(baseline, output / filename)
        failed = ratio > args.max_difference
        report.append({'file': filename, 'changed_ratio': ratio, 'failed': failed})
        if failed:
            shutil.copyfile(baseline, output / ('expected-' + filename))
            if diff is not None:
                diff.save(output / ('diff-' + filename))
            print(f'FAIL: {filename}: {ratio:.3%} changed pixels')
    (output / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    if any(item['failed'] for item in report):
        raise SystemExit('Visual changes detected. Inspect tools/visual-results; baselines were not modified.')
    print(f'PASS: {len(files)} visual comparisons at 390px and 1440px (limit {args.max_difference:.2%}).')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--update', action='store_true', help='Explicitly replace reviewed baselines')
    parser.add_argument('--output', type=Path, default=ROOT / 'tools/visual-results')
    parser.add_argument('--max-difference', type=float, default=.001, help='Allowed changed pixel fraction (default 0.1%%)')
    args = parser.parse_args()
    if not 0 <= args.max_difference <= 1:
        parser.error('--max-difference must be between 0 and 1')
    server = ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(QuietHandler, directory=str(ROOT)))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    try:
        asyncio.run(run(args, f'http://127.0.0.1:{server.server_port}'))
    finally:
        server.shutdown()
        server.server_close()


if __name__ == '__main__':
    main()
