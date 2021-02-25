/**
 * Handle the code related to the financer and instructor fields.
 *  - create the autocomplete fields using select2
 */

(function ($) {
    'use strict';
    $(document).ready(function () {

        const ctx = document.getElementById('chartAidsViewed').getContext('2d');
        const chartData = AID_VIEW_TIMESERIES;

        console.log(chartData)

        // Parse the dates to JS
        chartData.forEach((d) => {
            d.x = new Date(d.day);
        });

        console.log(chartData)

        // Render the chart
        const chart = new Chart(ctx, {
            plugins: [ChartDataLabels],
            type: 'bar',
            data: {
                datasets: [
                    {
                        data: chartData,
                        backgroundColor: '#DB1C83',
                    },
                ],
            },
            options: {
                responsive: true,
                layout: {
                    padding: {
                        top: 25,
                        left: 10,
                        right: 10,
                        bottom: 5
                    }
                },
                scales: {
                    xAxes: [
                        {
                            type: 'time',
                            time: {
                                unit: 'week',
                                isoWeekday: true,
                                // round: 'week',
                                tooltipFormat: 'll', // week
                            },
                            gridLines: {
                                display: false
                            },
                            offset: true
                        },
                    ],
                    yAxes: [
                        {
                            ticks: {
                                beginAtZero: true,
                                precision: 0
                            },
                        },
                    ],
                },
                legend: {
                    display: false
                },
                plugins: {
                    datalabels: {
                        formatter: function (value, context) {
                            return value.y;
                        },
                        anchor: 'end',
                        align: 'top',
                        font: {
                            weight: 'bold'
                        }
                    },
                },
            },
        });
    });
}($ || django.jQuery));
