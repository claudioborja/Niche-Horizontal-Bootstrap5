"""Exercise chart text alternatives, keyboard access and data synchronization."""
from pathlib import Path


async def check_chart_accessibility(page, visit):
    for path in ('index.html', 'index2.html', 'index3.html', 'index4.html',
                 'charts/chart-chart-js.html', 'charts/chart-morris.html',
                 'charts/chart-chartist.html', 'charts/chart-peity.html'):
        await visit(path)
        assert await page.evaluate('''() => Object.values(Chart.instances).every(chart => {
            const canvas = chart.canvas;
            if (canvas.getAttribute('role') !== 'img' || !canvas.getAttribute('aria-label')) return false;
            if (canvas.closest('[data-mini-chart]')) return canvas.getAttribute('aria-label').includes('Values:');
            const ids = canvas.getAttribute('aria-describedby').split(' ');
            const description = ids.map(id => document.getElementById(id)).find(el => el?.closest('.chart-data'));
            const table = description?.closest('.chart-data').querySelector('table');
            return table && table.caption.textContent && table.tHead.rows[0].cells.length === chart.data.datasets.length + 1
                && Array.from(table.tBodies[0].rows).every((row, index) => chart.data.datasets.every((dataset, column) =>
                    row.cells[column + 1].textContent === String(dataset.data[index])));
        })'''), path

    await visit('index.html')
    details = page.locator('.chart-data details').first
    summary = details.locator('summary')
    await summary.focus()
    await summary.press('Enter')
    assert await details.evaluate('el => el.open')
    assert await details.locator('table').is_visible()
    await page.evaluate("Chart.getChart('line-chart').data.datasets[0].data[0] = 987; Chart.getChart('line-chart').update('none')")
    assert await details.locator('tbody tr').first.locator('td').first.text_content() == '987'
    assert await summary.evaluate('el => el === document.activeElement')
    await page.evaluate("Chart.getChart('line-chart').hide(0)")
    assert 'hidden in chart' in await details.locator('thead th').nth(1).text_content()
    assert await details.locator('tbody tr').count() == 7
    await summary.press('Space')
    assert not await details.evaluate('el => el.open')
    await page.evaluate('''() => {
        const chart = Chart.getChart('line-chart');
        const canvas = chart.canvas;
        chart.destroy();
        new Chart(canvas, {type: 'bar', data: {labels: ['Replacement'], datasets: [{label: 'New series', data: [5]}]}, options: {animation: false}});
    }''')
    assert await page.locator('.chart-data').count() == 3
    assert await page.locator('.chart-data').first.locator('tbody').text_content() == 'Replacement5'

    await page.set_viewport_size({'width': 390, 'height': 844})
    await visit('charts/chart-chartist.html')
    details = page.locator('.chart-data details').nth(2)
    await details.locator('summary').focus()
    await details.locator('summary').press('Enter')
    await details.locator('summary').press('Tab')
    assert await details.locator('.chart-data-scroll').evaluate('el => el === document.activeElement')
    assert await page.evaluate('document.documentElement.scrollWidth <= innerWidth')
    await page.add_script_tag(path=str(Path(__file__).resolve().parent / 'test-vendor/axe-core-4.13.0/axe.min.js'))
    assert await page.evaluate("axe.run(document.querySelectorAll('.chart-data'), {runOnly: ['color-contrast', 'aria-valid-attr-value', 'table-fake-caption', 'td-has-header', 'th-has-data-cells']}).then(result => result.violations.length)") == 0

    await visit('charts/chart-peity.html')
    assert await page.locator('[data-mini-chart="pie"][data-values="1/5"] canvas').get_attribute('aria-label') == 'Pie chart. Ratio 1 of 5. Values: 1, 4.'
    assert await page.evaluate("[...document.querySelectorAll('[data-mini-chart] canvas')].some(el => el.getAttribute('aria-label').includes('-7'))")
    await visit('charts/chart-knob.html')
    gauge = page.locator('input.knob').nth(1)
    await gauge.press('ArrowUp')
    assert await gauge.input_value() == '76'
    assert await page.locator('#niche-gauge-value-1').text_content() == 'Value: 76. Range: 0 to 100.'
    assert await page.evaluate("[...document.querySelectorAll('input.knob')].every(el => document.getElementById(el.getAttribute('aria-describedby')).textContent.includes('Value:'))")
    assert await page.evaluate("[...document.querySelectorAll('input.knob')].every(el => [...el.parentElement.querySelectorAll('canvas')].every(canvas => canvas.getAttribute('aria-hidden') === 'true'))")
    await page.set_viewport_size({'width': 1440, 'height': 1000})
    print('PASS: chart summaries/tables expose actual data, update with hidden/changed series, open by keyboard and fit mobile; mini charts and gauges expose their values.', flush=True)
