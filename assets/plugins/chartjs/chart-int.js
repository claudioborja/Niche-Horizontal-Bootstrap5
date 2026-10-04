document.addEventListener('DOMContentLoaded', async function () {
    'use strict';
    if (!window.Chart) return;
    await document.fonts.load('12px ' + Chart.defaults.font.family);

    var labels = ['January', 'February', 'March', 'April', 'May', 'June'];
    var values = [12, 19, 8, 15, 10, 17];
    var colors = ['#398bf7', '#06d79c', '#ffb22b', '#ef5350', '#745af2', '#26c6da'];
    var charts = [
        { id: 'line-chart', type: 'line' },
        { id: 'bar-chart', type: 'bar' },
        { id: 'pie-chart', type: 'pie' },
        { id: 'doughnut-chart', type: 'doughnut' },
        { id: 'polararea-chart', type: 'polarArea' },
        { id: 'radar-chart', type: 'radar' }
    ];

    charts.forEach(function (chart) {
        var canvas = document.getElementById(chart.id);
        if (!canvas) return;

        var cartesian = chart.type === 'line' || chart.type === 'bar';
        new Chart(canvas, {
            type: chart.type,
            data: {
                labels: labels,
                datasets: [{
                    label: 'Sales',
                    data: values.slice(),
                    backgroundColor: chart.type === 'line' || chart.type === 'radar'
                        ? 'rgba(57, 139, 247, 0.2)' : colors,
                    borderColor: cartesian || chart.type === 'radar' ? '#398bf7' : '#fff',
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                plugins: { legend: { display: !cartesian } },
                scales: cartesian ? { y: { beginAtZero: true } } : {}
            }
        });
    });
});
