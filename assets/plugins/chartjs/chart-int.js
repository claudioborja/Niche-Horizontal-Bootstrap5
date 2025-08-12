/*
Template Name: Niche
Author: UXLiner
*/
$(document).ready(function() {
    "use strict";

    // Verificar que Chart.js está disponible
    if (typeof Chart === 'undefined') {
        console.error('Chart.js no está cargado');
        return;
    }

    console.log('Inicializando gráficos con Chart.js v4');

// ======
// line chart
// ======	
var lineChartElement = document.getElementById('line-chart');
if (lineChartElement) {
    var ctx = lineChartElement.getContext('2d');
    var chart = new Chart(ctx, {
        // The type of chart we want to create
        type: 'line',

        // The data for our dataset
        data: {
            labels: ["January", "February", "March", "April", "May", "June", "July"],
            datasets: [{
               label: "Sales",
                borderColor: 'rgb(88, 103, 221)',
                backgroundColor: 'rgba(88, 103, 221, 0.1)',
                data: [0, 10, 5, 2, 20, 30, 45],
                fill: false,
                tension: 0.1
                    }, {
              label: "Earning",
                borderColor: 'rgb(0, 140, 211)',
                backgroundColor: 'rgba(0, 140, 211, 0.1)',
                data: [15, 15, 10, 20, 30, 10, 25],
                fill: false,
                tension: 0.1
                    }]
                },
    	options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: true,
                        position: 'top'
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
    });
    console.log('Line chart created successfully');
}

// ======
// Pie chart
// ======
var pieChartElement = document.getElementById("pie-chart");
if (pieChartElement) {
    new Chart(pieChartElement,{
    	type:'pie',
    	data:{
    		labels: ['Desktop', 'Mobile', 'Tablet'],
    		datasets:[{
    		    label:'Visitors',
        		data: [300, 50, 100],
        		backgroundColor: [
        			'rgb(255, 99, 132)',
        			'rgb(54, 162, 235)',
        			'rgb(255, 205, 86)'
        		],
        		borderWidth: 2,
        		borderColor: '#fff'
    		}]
    	},
    	options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: 'bottom'
                },
                tooltip: {
                    enabled: true
                }
            }
        }
    });
    console.log('Pie chart created successfully');
}

    console.log('Todos los gráficos se han inicializado correctamente');
});