/* Compact Chart.js charts, with the original inline demo data. */
document.addEventListener('DOMContentLoaded', async function () {
    'use strict';
    if (!window.Chart) return;
    await document.fonts.load('12px ' + Chart.defaults.font.family);
    document.querySelectorAll('[data-mini-chart]').forEach(function (host) {
        const type = host.dataset.miniChart;
        const raw = host.dataset.values;
        let values = raw.split(/[,/]/).map(Number);
        if (raw.includes('/')) values = [values[0], Math.max(0, values[1] - values[0])];
        const settings = JSON.parse(host.dataset.chartOptions || '{}');
        const circular = type === 'pie' || type === 'doughnut';
        const width = host.dataset.width || (circular ? 64 : 100);
        host.style.width = width === '100%' ? width : width + 'px';
        host.style.height = (host.dataset.height || (circular ? 64 : 40)) + 'px';
        host.classList.add('mini-chart');
        const canvas = document.createElement('canvas');
        canvas.setAttribute('role', 'img');
        canvas.setAttribute('aria-label', type + ' chart: ' + raw);
        canvas.textContent = raw;
        host.replaceChildren(canvas);
        new Chart(canvas, {
            type: type,
            data: {
                labels: values.map(function (_, index) { return String(index + 1); }),
                datasets: [{
                    data: values,
                    backgroundColor: settings.fill || (circular ? ['#009efb', '#f2f2f2'] : '#009efb'),
                    borderColor: type === 'line' ? '#009efb' : undefined,
                    borderWidth: type === 'line' ? 1 : 0,
                    pointRadius: 0,
                    fill: type === 'line'
                }]
            },
            options: {
                responsive: true, maintainAspectRatio: false, animation: false,
                cutout: type === 'doughnut' ? (settings.innerRadius || 16) / (settings.radius || 32) * 100 + '%' : 0,
                plugins: { legend: { display: false }, tooltip: { enabled: true } },
                scales: circular ? {} : { x: { display: false }, y: { display: false, beginAtZero: true } }
            }
        });
    });
});
