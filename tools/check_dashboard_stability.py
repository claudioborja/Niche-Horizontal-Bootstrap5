"""Check dashboard layout with delayed fonts and chart initialization."""
import asyncio


async def check_dashboard_stability(browser, base_url):
    for width, height in ((1350, 940), (390, 844)):
        context = await browser.new_context(viewport={'width': width, 'height': height}, reduced_motion='reduce')
        page = await context.new_page()
        release = asyncio.Event()

        async def delay_charts(route):
            await release.wait()
            await route.continue_()

        async def delay_font(route):
            await asyncio.sleep(0.6)
            await route.continue_()

        try:
            await page.route('**/assets/js/dashboard-charts.js', delay_charts)
            await page.route('**/*.woff2*', delay_font)
            await page.add_init_script('''window.testShifts = [];
                new PerformanceObserver(list => {
                    for (const entry of list.getEntries()) {
                        if (!entry.hadRecentInput) testShifts.push(entry.value);
                    }
                }).observe({type: 'layout-shift', buffered: true});''')
            await page.goto(base_url + '/index.html', wait_until='commit')
            await page.locator('.chart-data[data-chart-for]').last.wait_for()
            assert await page.locator('.chart-data[aria-busy=true]').count() == 3
            await page.evaluate('document.fonts.ready')
            await page.evaluate('''() => new Promise(resolve => requestAnimationFrame(() => {
                window.testInitialPanels = [...document.querySelectorAll('.chart-data[data-chart-for]')];
                window.testCardPositions = testInitialPanels.map(panel =>
                    panel.getBoundingClientRect().top - document.querySelector('#main-content').getBoundingClientRect().top);
                requestAnimationFrame(resolve);
            }))''')
            await page.locator('.chart-data summary').first.focus()
            release.set()
            await page.wait_for_function('window.Chart && Object.keys(Chart.instances).length === 3')
            await page.wait_for_function('!document.querySelector(".chart-data[aria-busy=true]")')
            await page.wait_for_timeout(300)
            assert await page.evaluate('''() => testInitialPanels.every((panel, index) =>
                panel === document.querySelectorAll('.chart-data[data-chart-for]')[index]
                && panel.querySelector('table tbody tr')
                && Math.abs(panel.getBoundingClientRect().top
                    - document.querySelector('#main-content').getBoundingClientRect().top
                    - testCardPositions[index]) <= 1)'''), f'Chart initialization moves/replaces reserved panels at {width}px'
            shifts = await page.evaluate('testShifts.reduce((total, value) => total + value, 0)')
            assert await page.locator('.chart-data summary').first.evaluate('el => el === document.activeElement'), 'Chart initialization loses keyboard focus'
            assert shifts < 0.05, f'Delayed dashboard CLS {shifts:.3f} at {width}px'
            print(f'PASS: delayed dashboard fonts/charts preserve reserved panels at {width}px; CLS {shifts:.3f}.', flush=True)
        finally:
            release.set()
            await context.close()
