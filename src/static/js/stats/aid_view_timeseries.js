/**
 * Handle the code related to the financer and instructor fields.
 *  - create the autocomplete fields using select2
 */

(function ($) {
    'use strict';
    $(document).ready(function () {

        const ctx = document.getElementById('chartAidsViewed').getContext('2d');
        const chartData = AID_VIEW_TIMESERIES;

        const LOCALE = 'fr-FR';
        const localeDateStringOptions = { day: 'numeric', month: 'numeric' };

        function customWeekLabel(date) {
            var weekStartDate = new Date(date);
            var weekStartDateStr = weekStartDate.toLocaleString(LOCALE, localeDateStringOptions);
            var weekEndDate = new Date(date);
            weekEndDate.setDate(weekStartDate.getDate() + 6);
            var weekEndDateStr = weekEndDate.toLocaleString(LOCALE, localeDateStringOptions);
            return weekStartDateStr + ' > ' + weekEndDateStr;
        }

        // Parse the dates to JS
        chartData.forEach((d) => {
            // set x
            d.x = new Date(d.day);
            // build xLabel
            
        });

        // Render the chart
        const chart = new Chart(ctx, {
            plugins: [ChartDataLabels],
            type: 'bar',
            data: {
                datasets: [{
                    data: chartData,
                    backgroundColor: '#DB1C83',
                }],
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
                    xAxes: [{
                        type: 'time',
                        time: {
                            unit: 'week',
                            isoWeekday: true,
                            // tooltipFormat: 'll', // week
                        },
                        gridLines: {
                            display: false
                        },
                        offset: true,
                        ticks: {
                            callback: function(date, index, values) {
                                return customWeekLabel(date);
                            }
                        },
                    }],
                    yAxes: [{
                        ticks: {
                            beginAtZero: true,
                            precision: 0,
                        },
                    }],
                },
                tooltips: {
                    callbacks: {
                        title: function(tooltipItems, data) {
                            return customWeekLabel(tooltipItems[0].xLabel);
                        },
                        label: function(tooltipItem, data) {
                            return tooltipItem.yLabel + ' vue' + (tooltipItem.yLabel > 1 ? 's' : '');
                        },
                  }
                },
                legend: {
                    display: false
                },
                plugins: {
                    // to have y labels on top of the bars
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
