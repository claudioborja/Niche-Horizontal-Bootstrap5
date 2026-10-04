/* Text alternatives use the same data as the canvas and follow chart.update(). */
(function () {
    'use strict';
    if (!window.Chart) return;
    const states = new WeakMap();
    const types = { line: 'Line', bar: 'Bar', pie: 'Pie', doughnut: 'Doughnut', polarArea: 'Polar area', radar: 'Radar' };

    function element(tag, text, className) {
        const node = document.createElement(tag);
        if (text !== undefined) node.textContent = text;
        if (className) node.className = className;
        return node;
    }

    function valueText(value) {
        if (value === null || value === undefined) return 'No data';
        if (Array.isArray(value)) return value.map(valueText).join(' to ');
        if (typeof value === 'object') return Object.entries(value).map(([key, item]) => key + ': ' + valueText(item)).join(', ');
        return String(value);
    }

    function update(chart) {
        const canvas = chart.canvas;
        const mini = canvas.closest('[data-mini-chart]');
        const type = types[chart.config.type] || chart.config.type;
        const datasets = chart.data.datasets;
        const count = Math.max(chart.data.labels.length, ...datasets.map(dataset => dataset.data.length));
        const labels = Array.from({ length: count }, (_, index) => valueText(chart.data.labels[index] ?? index + 1));
        canvas.setAttribute('role', 'img');
        if (mini) {
            // Compact charts retain their size; all values are in their accessible name.
            const ratio = mini.dataset.values.includes('/') ? ' Ratio ' + mini.dataset.values.replace('/', ' of ') + '.' : '';
            canvas.setAttribute('aria-label', type + ' chart.' + ratio + ' Values: ' + datasets.map(dataset => dataset.data.map(valueText).join(', ')).join('; ') + '.');
            return;
        }
        let state = states.get(chart);
        if (!state) {
            const heading = canvas.closest('.info-box')?.querySelector('h4, h5');
            const title = heading?.textContent.trim() || canvas.getAttribute('aria-label') || type + ' chart';
            let id = 'niche-chart-data-' + chart.id;
            while (document.getElementById(id)) id += '-data';
            const panel = element('div', undefined, 'chart-data');
            const description = element('p', undefined, 'chart-data-description');
            description.id = id;
            const details = element('details');
            const summary = element('summary', 'View chart data: ' + title);
            const scroll = element('div', undefined, 'chart-data-scroll');
            scroll.tabIndex = 0;
            scroll.setAttribute('role', 'region');
            scroll.setAttribute('aria-label', title + ' data table');
            details.append(summary, scroll);
            panel.append(description, details);
            // Keep the table outside the canvas sizing wrapper to avoid resize loops.
            canvas.parentElement.after(panel);
            state = { canvas, panel, description, scroll, title, signature: '' };
            states.set(chart, state);
            canvas.setAttribute('aria-label', title + '. ' + type + ' chart.');
            const describedBy = new Set((canvas.getAttribute('aria-describedby') || '').split(/\s+/).filter(Boolean));
            describedBy.add(id);
            canvas.setAttribute('aria-describedby', [...describedBy].join(' '));
        }
        const names = datasets.map((dataset, index) => dataset.label || (datasets.length === 1 ? 'Value' : 'Series ' + (index + 1)));
        const hidden = datasets.map((_, index) => !chart.isDatasetVisible(index));
        const hiddenRows = labels.map((_, index) => !chart.getDataVisibility(index));
        const signature = JSON.stringify([labels, datasets.map(dataset => dataset.data), names, hidden, hiddenRows]);
        if (signature === state.signature) return;
        state.signature = signature;
        state.description.textContent = type + ' chart with ' + count + ' categories and ' + datasets.length + ' series: ' + names.join(', ') + '. The table includes all values, including any hidden in the chart.';
        const table = element('table', undefined, 'table table-sm');
        table.append(element('caption', state.title + ' — chart data'));
        const head = element('thead');
        const headers = element('tr');
        ['Category', ...names.map((name, index) => name + (hidden[index] ? ' (hidden in chart)' : ''))].forEach(name => {
            const cell = element('th', name);
            cell.scope = 'col';
            headers.append(cell);
        });
        head.append(headers);
        const body = element('tbody');
        labels.forEach((label, index) => {
            const row = element('tr');
            const header = element('th', label + (hiddenRows[index] ? ' (hidden in chart)' : ''));
            header.scope = 'row';
            row.append(header);
            datasets.forEach(dataset => row.append(element('td', valueText(dataset.data[index]))));
            body.append(row);
        });
        table.append(head, body);
        state.scroll.replaceChildren(table);
    }

    Chart.register({
        id: 'niche-chart-accessibility',
        afterUpdate: update,
        afterDestroy: function (chart) {
            const state = states.get(chart);
            if (!state) return;
            const ids = (state.canvas.getAttribute('aria-describedby') || '').split(/\s+/).filter(id => id && id !== state.description.id);
            if (ids.length) state.canvas.setAttribute('aria-describedby', ids.join(' '));
            else state.canvas.removeAttribute('aria-describedby');
            state.panel.remove();
            states.delete(chart);
        }
    });
})();
