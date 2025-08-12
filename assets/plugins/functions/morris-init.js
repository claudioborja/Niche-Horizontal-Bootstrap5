/*
Template Name: Niche
Author: UXLiner
*/
(function($) {
    "use strict";

    $(document).ready(function() {
        // Check if Morris is loaded
        if (typeof Morris === 'undefined') {
            console.warn('Morris.js is not loaded');
            return;
        }

        // ======
        // Yearly Earning Starts
        // ======
        if ($('#earning').length > 0) {
            var day_data = [
                {"elapsed": "2012", "Sales": 60, "Earning": 80},
                {"elapsed": "2013", "Sales": 100, "Earning": 130},
                {"elapsed": "2014", "Sales": 70, "Earning": 50},
                {"elapsed": "2015", "Sales": 80, "Earning": 155},
                {"elapsed": "2016", "Sales": 155, "Earning": 105},
                {"elapsed": "2017", "Sales": 120, "Earning": 110},
                {"elapsed": "2018", "Sales": 250, "Earning": 180}
            ];
            Morris.Line({
                element: 'earning',
                data: day_data,
                xkey: 'elapsed',
                ykeys: ['Sales', 'Earning'],
                labels: ['Sales', 'Earning'],
                fillOpacity: 0,
                pointStrokeColors: ['#1976d2', '#26c6da'],
                behaveLikeLine: true,
                gridLineColor: '#e0e0e0',
                lineWidth: 3,
                hideHover: 'auto',
                lineColors: ['#5867dd', '#008cd3'],
                resize: true
            });
        }

        // ======
        // Area Chart Starts
        // ======
        if ($('#area').length > 0) {
            Morris.Area({
                element: 'area',
                data: [
                    {x: '2013', india: 100, usa: 30, uk: 10},
                    {x: '2014', india: 20, usa: 110, uk: 90},
                    {x: '2015', india: 120, usa: 35, uk: 15},
                    {x: '2016', india: 60, usa: 90, uk: 70},
                    {x: '2017', india: 130, usa: 40, uk: 20},
                    {x: '2018', india: 60, usa: 80, uk: 5}
                ],
                xkey: 'x',
                ykeys: ['india', 'usa', 'uk'],
                labels: ['India', 'USA', 'UK'],
                fillOpacity: 0.9,
                pointStrokeColors: ['#778dcd', '#7088cc', '#2d3ec3'],
                behaveLikeLine: true,
                gridLineColor: '#e0e0e0',
                lineWidth: 0,
                smooth: true,
                hideHover: 'auto',
                lineColors: ['#4d64a7', '#778dcd', '#2d3ec3'],
                resize: true
            });
        }

        // ======
        // Donut Chart Starts
        // ======
        if ($('#donut').length > 0) {
            Morris.Donut({
                element: 'donut',
                data: [
                    {value: 40, label: 'In-Store Sales'},
                    {value: 25, label: 'Mail-Order Sales'},
                    {value: 20, label: 'Download Sales'},
                    {value: 15, label: 'Latest Order'}
                ],
                backgroundColor: '#fff',
                labelColor: '#404e67',
                colors: [
                    '#ff4558',
                    '#ff7d4d',
                    '#00a5a8',
                    '#626e82'
                ],
                formatter: function (x) { return x + "%"; }
            });
        }

        // ======
        // Bar chart Start
        // ======
        if ($('#bar-chart').length > 0) {
            Morris.Bar({
                element: 'bar-chart',
                data: [
                    {x: '2011', y: 60, z: 20, a: 40},
                    {x: '2012', y: 20, z: 50, a: 10},
                    {x: '2013', y: 10, z: 50, a: 35},
                    {x: '2014', y: 20, z: 40, a: 20}
                ],
                xkey: 'x',
                ykeys: ['y', 'z', 'a'],
                labels: ['Y', 'Z', 'A'],
                resize: true
            }).on('click', function(i, row){
                console.log(i, row);
            });
        }
    });

})(jQuery);