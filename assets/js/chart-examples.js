/* Chart.js examples shared by the dashboards and chart galleries. */
document.addEventListener('DOMContentLoaded', function () {
    'use strict';

    var colors = ['#5867dd', '#008cd3', '#26c6da', '#ff7d4d', '#ff4558', '#626e82', '#06d79c'];
    var reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    function series(labels, values, names, fill) {
        return {
            labels: labels,
            datasets: values.map(function (data, index) {
                return {
                    label: names[index], data: data,
                    borderColor: colors[index % colors.length],
                    backgroundColor: fill ? colors[index % colors.length] + '40' : colors[index % colors.length],
                    borderWidth: 2, pointRadius: 3, tension: 0.3, fill: Boolean(fill)
                };
            })
        };
    }

    function draw(selector, type, data, extra) {
        var canvas = document.querySelector(selector);
        if (!canvas) return;
        var options = Object.assign({
            responsive: true, maintainAspectRatio: false,
            animation: reducedMotion ? false : { duration: 1000 },
            plugins: { legend: { position: 'bottom' } }
        }, extra || {});
        if (type === 'line' || type === 'bar') {
            options.scales = { y: { beginAtZero: true } };
        }
        new Chart(canvas, { type: type, data: data, options: options });
    }

    draw('#earning', 'line', series(
        ['2012', '2013', '2014', '2015', '2016', '2017', '2018'],
        [[60, 100, 70, 80, 155, 120, 250], [80, 130, 50, 155, 105, 110, 180]],
        ['Sales', 'Earning'], false
    ));
    draw('#area', 'line', series(
        ['2013', '2014', '2015', '2016', '2017', '2018'],
        [[100, 20, 120, 60, 130, 60], [30, 110, 35, 90, 40, 80], [10, 90, 15, 70, 20, 5]],
        ['India', 'USA', 'UK'], true
    ));
    draw('#donut', 'doughnut', {
        labels: ['In-Store Sales', 'Mail-Order Sales', 'Download Sales', 'Latest Order'],
        datasets: [{ data: [40, 25, 20, 15], backgroundColor: ['#ff4558', '#ff7d4d', '#00a5a8', '#626e82'] }]
    }, {
        plugins: {
            legend: { position: 'bottom' },
            tooltip: { callbacks: { label: function (context) { return context.label + ': ' + context.parsed + '%'; } } }
        }
    });
    draw('#bar-chart', 'bar', series(
        ['2011', '2012', '2013', '2014'],
        [[60, 20, 10, 20], [20, 50, 50, 40], [40, 10, 35, 20]], ['Y', 'Z', 'A'], false
    ));

    draw('.ct-line-chart', 'line', series(
        ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
        [[12, 9, 7, 8, 5], [2, 1, 3.5, 7, 3], [1, 3, 4, 5, 6]],
        ['Series 1', 'Series 2', 'Series 3'], false
    ));
    draw('.ct-line-area-chart', 'line', series(
        ['1', '2', '3', '4', '5', '6', '7', '8'], [[5, 9, 7, 8, 5, 3, 5, 4]], ['Series 1'], true
    ));
    draw('.ct-animation-chart', 'line', series(
        ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'],
        [[12, 9, 7, 8, 5, 4, 6, 2, 3, 3, 4, 6], [4, 5, 3, 7, 3, 5, 5, 3, 4, 4, 5, 5],
         [5, 3, 4, 5, 6, 3, 3, 4, 5, 6, 3, 4], [3, 4, 5, 6, 7, 6, 4, 5, 6, 7, 6, 3]],
        ['Series 1', 'Series 2', 'Series 3', 'Series 4'], false
    ), { animation: reducedMotion ? false : {
        duration: 1000,
        delay: function (context) { return context.type === 'data' && context.mode === 'default' ? context.dataIndex * 80 : 0; }
    } });
    draw('.ct-bar-chart', 'bar', series(
        ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        [[5, 4, 3, 7, 5, 10, 3, 4, 8, 10, 6, 8], [3, 2, 9, 5, 4, 6, 4, 6, 7, 8, 7, 4]],
        ['Series 1', 'Series 2'], false
    ));
    draw('.ct-svg-path-chart', 'line', series(
        ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'],
        [[1, 5, 2, 5, 4, 3], [2, 3, 4, 8, 1, 2], [5, 4, 3, 2, 1, 0.5]],
        ['Series 1', 'Series 2', 'Series 3'], true
    ), { animation: reducedMotion ? false : { duration: 2000 } });
    draw('.ct-gauge-chart', 'doughnut', {
        labels: ['Series 1', 'Series 2', 'Series 3', 'Series 4'],
        datasets: [{ data: [20, 10, 30, 40], backgroundColor: colors.slice(0, 4) }]
    }, { rotation: -90, circumference: 180, cutout: '60%' });
    draw('.ct-donute-chart', 'doughnut', {
        labels: ['1', '2', '3', '4', '5', '6', '7'],
        datasets: [{ data: [10, 20, 50, 20, 5, 50, 15], backgroundColor: colors }]
    }, { animation: reducedMotion ? false : { duration: 1500, animateRotate: true } });
});
