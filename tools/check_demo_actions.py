"""Ensure demo notices do not intercept working widgets or send form requests."""
from pathlib import Path


async def check_demo_actions(page, visit):
    await visit('index.html')
    footer = page.locator('.main-footer')
    assert await footer.get_by_role('link', name='Home', exact=True).get_attribute('href') == 'index.html'
    await page.evaluate('window.scrollTo(0, 300)')
    await footer.get_by_role('button', name='About (demo)', exact=True).focus()
    before = await page.evaluate('scrollY')
    await page.keyboard.press('Enter')
    assert await page.locator('.demo-status').is_visible()
    assert await page.evaluate('scrollY') == before
    assert not page.url.endswith('#')
    await page.get_by_role('button', name='Close demo notice').click()
    assert not await page.locator('.demo-status').is_visible()
    await page.keyboard.press('Space')
    assert await page.locator('.demo-status').is_visible()
    await page.fill('.search-form input', 'Example')
    await page.locator('.search-form button').click()
    assert 'No search service' in await page.locator('.demo-status').text_content()
    await page.set_viewport_size({'width': 390, 'height': 844})
    assert await page.locator('.demo-status').evaluate('el => {const r = el.getBoundingClientRect(); return r.left >= 0 && r.right <= innerWidth;}')
    await page.add_script_tag(path=str(Path(__file__).resolve().parent / 'test-vendor/axe-core-4.13.0/axe.min.js'))
    assert await page.evaluate("axe.run(document.querySelector('.demo-status'), {runOnly: ['color-contrast', 'button-name', 'aria-valid-attr-value']}).then(result => result.violations.length)") == 0

    await visit('pages/pages-login.html')
    requests = []
    listener = lambda request: requests.append(request.url) if request.is_navigation_request() else None
    page.on('request', listener)
    assert await page.locator('.demo-form-note').is_visible()
    await page.fill('#email', 'demo@example.com')
    await page.fill('#password', 'example-password')
    await page.locator('button[type=submit]').click()
    assert 'No information was sent' in await page.locator('.demo-status').text_content()
    assert not requests
    assert page.url.endswith('/pages/pages-login.html')
    page.remove_listener('request', listener)

    await visit('apps/apps-compose-mail.html')
    await page.locator('[data-demo-message^="Demo message"]').click()
    assert 'No email was sent' in await page.locator('.demo-status').text_content()
    await page.locator('[data-demo-message^="Demo draft"]').click()
    assert 'not saved' in await page.locator('.demo-status').text_content()

    await visit('tables/table-data-table.html')
    button = page.get_by_role('button', name='Export CSV', exact=True).first
    assert await button.get_attribute('data-demo-action') is None
    async with page.expect_download() as download:
        await button.click()
    assert (await download.value).suggested_filename.endswith('.csv')
    assert await page.locator('.demo-status').count() == 0
    await page.set_viewport_size({'width': 1440, 'height': 1000})
    print('PASS: placeholder links/search show accessible notices without jumping; auth/mail demos send no requests; CSV export remains functional.', flush=True)
