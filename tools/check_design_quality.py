"""Exercise responsive layout and hit areas in the real template pages."""
from urllib.parse import urlsplit


async def check_design(page, visit):
    # Slow/unavailable scripts must not change the initial navigation footprint.
    initial = await page.context.new_page()
    try:
        for path, width in (('index.html', 390), ('index.html', 1440),
                            ('pages/pages-blank.html', 390), ('pages/pages-blank.html', 1440)):
            await initial.set_viewport_size({'width': width, 'height': 900})
            await initial.route('**/*.js', lambda route: route.abort())
            url = urlsplit(page.url)
            await initial.goto(f'{url.scheme}://{url.netloc}/{path}')
            await initial.evaluate('document.fonts.ready')
            before = await initial.locator('#main-content').evaluate('el => el.getBoundingClientRect().top')
            footer_before = await initial.locator('.main-footer .row').first.evaluate('el => el.getBoundingClientRect().top')
            await initial.unroute('**/*.js')
            await initial.reload()
            await initial.evaluate('document.fonts.ready')
            after = await initial.locator('#main-content').evaluate('el => el.getBoundingClientRect().top')
            assert abs(after - before) <= 3, f'Navigation shifts content by {after - before}px at {width}px'
            if 'blank' in path:
                footer_after = await initial.locator('.main-footer .row').first.evaluate('el => el.getBoundingClientRect().top')
                assert abs(footer_after - footer_before) <= 3, f'Layout shifts footer by {footer_after - footer_before}px at {width}px'
    finally:
        await initial.close()
    print('PASS: navigation and blank-page footer stay within 3px of their initial position when scripts load.', flush=True)
    for width in (320, 390, 768, 1440):
        await page.set_viewport_size({'width': width, 'height': 900})
        await visit('index.html')
        await page.evaluate('document.fonts.ready')
        assert await page.evaluate("""() => {
            const input = document.querySelector('.search-form input').getBoundingClientRect();
            const account = document.querySelector('.user-menu > a').getBoundingClientRect();
            return input.width >= 90 && input.left >= 0 && account.right <= innerWidth + 1;
        }"""), f'Header does not fit at {width}px'
        if width < 768:
            await page.locator('.user-menu > a').click()
            assert await page.locator('.user-menu > .dropdown-menu').evaluate("""el => {
                const r = el.getBoundingClientRect();
                return r.left >= 0 && r.right <= innerWidth + 1;
            }"""), f'Account dropdown does not fit at {width}px'
        await visit('ui/ui-horizontal-timeline.html')
        assert await page.locator('.events-content').evaluate("""el => {
            const r = el.getBoundingClientRect();
            return r.left >= 0 && r.right <= innerWidth && r.width <= 800;
        }"""), f'Timeline does not fit at {width}px'

    # Resize an already loaded desktop page, rather than only loading at mobile sizes.
    await visit('index.html')
    await page.set_viewport_size({'width': 320, 'height': 844})
    assert await page.evaluate("""() => [...document.querySelectorAll(
        '.main-header .logo, .main-header .navbar, .search-form input, .user-menu > a'
    )].every(el => { const r = el.getBoundingClientRect(); return r.left >= 0 && r.right <= innerWidth + 1; })"""), 'Header clips during a desktop-to-mobile resize'

    await page.set_viewport_size({'width': 390, 'height': 844})
    await visit('apps/apps-mailbox.html')
    star = page.locator('.mailbox-star > a').first
    label = page.locator('.mailbox-select').first
    for target in (star, label):
        assert await target.evaluate('el => { const r = el.getBoundingClientRect(); return r.width >= 44 && r.height >= 44; }')
    initial = await star.get_attribute('aria-label')
    await star.click()
    assert await star.get_attribute('aria-label') != initial
    # Click the label edge, outside the 18px checkbox, to exercise the hit area.
    await label.click(position={'x': 3, 'y': 3})
    assert await label.locator('input').is_checked()
    await label.click(position={'x': 3, 'y': 3})
    assert not await label.locator('input').is_checked()

    await visit('apps/apps-calendar.html')
    assert await page.evaluate("testCalendars.every(c => c.view.type === 'timeGridDay')")
    await page.locator('#calendar button[role=tab]').filter(has_text='Month').click()
    assert await page.evaluate("testCalendars[0].view.type === 'dayGridMonth'")
    await page.set_viewport_size({'width': 1440, 'height': 1000})
    await page.wait_for_function("testCalendars.every(c => c.view.type === 'dayGridMonth')")
    await page.locator('#calendar button[role=tab]').filter(has_text='Week').click()
    await page.set_viewport_size({'width': 390, 'height': 844})
    await page.wait_for_function("testCalendars.every(c => c.view.type === 'timeGridDay')")
    await page.set_viewport_size({'width': 320, 'height': 844})
    assert await page.evaluate("testCalendars.every(c => c.view.type === 'timeGridDay')")
    await page.set_viewport_size({'width': 1440, 'height': 1000})
    await page.wait_for_function("testCalendars[0].view.type === 'timeGridWeek' && testCalendars[1].view.type === 'dayGridMonth'")
    print('PASS: header/timeline fit 320–1440px, mailbox hit areas activate their controls, and calendars preserve desktop view choices.', flush=True)
    await check_theme(page, visit)


async def check_theme(page, visit):
    # Exercise actual customization through the shared variables, including aliases.
    await visit('index3.html')
    await page.evaluate("""() => {
        const theme = document.documentElement.style;
        for (const [name, value] of Object.entries({
            '--niche-color-primary': '#233b6e', '--niche-color-link': '#202020',
            '--niche-font-size-base': '18px', '--niche-card-padding': '28px',
            '--niche-radius-card': '12px'
        })) theme.setProperty(name, value);
    }""")
    await page.wait_for_function("getComputedStyle(document.querySelector('.content-header .breadcrumb a')).color === 'rgb(32, 32, 32)'")
    assert await page.evaluate("""() => {
        const header = getComputedStyle(document.querySelector('.navbar.blue-bg'));
        const link = getComputedStyle(document.querySelector('.content-header .breadcrumb a'));
        const card = getComputedStyle(document.querySelector('.info-box'));
        return header.backgroundColor === 'rgb(35, 59, 110)' && link.color === 'rgb(32, 32, 32)'
            && getComputedStyle(document.body).fontSize === '18px'
            && card.paddingTop === '28px' && card.borderRadius === '12px';
    }"""), 'Shared theme changes do not reach the rendered components'
    await visit('ui/ui-buttons.html')
    await page.evaluate("""() => {
        document.documentElement.style.setProperty('--niche-button-padding-x', '32px');
        document.documentElement.style.setProperty('--niche-radius-button', '9px');
    }""")
    assert await page.locator('.info-box .btn-primary').first.evaluate("""el => {
        const button = getComputedStyle(el);
        return button.paddingLeft === '32px' && button.borderRadius === '9px';
    }"""), 'Shared button variables do not reach the rendered buttons'
    await visit('pages/pages-gallery.html')
    await page.evaluate("document.documentElement.style.setProperty('--niche-space-5', '28px')")
    assert await page.locator('.gallery-grid').evaluate("el => getComputedStyle(el).gap === '28px'")
    print('PASS: shared theme customizes brand/link colors, typography, card/button shapes and spacing, and gallery gaps.', flush=True)
