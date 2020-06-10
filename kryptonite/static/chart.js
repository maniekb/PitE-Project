const endpoint = '/api/data/chart'

const colors = ['rgba(255, 0, 0, 0.6)', 'rgba(44, 130, 201, 1)', 'rgba(245, 229, 27, 1)',
    'rgba(0,255,0,0.36)', 'rgba(255,111,0,0.84)', 'rgba(119,0,255,0.83)', 'rgba(54, 215, 183, 1)']
let charts = {};

class Currency {
    data = []
    labels = []

    constructor(symbol) {
        this.symbol = symbol
    }
}

const currencies_data = JSON.parse(document.getElementById('currencies_data').textContent);
const exchanges_data = JSON.parse(document.getElementById('exchanges_data').textContent);
let symbols = []
currencies_data.forEach(function (currency) {
    symbols.push(currency['value']);
})

let getDataContainers = function (symbols) {
    let dataContainers = []
    for (let i = 0; i < symbols.length; ++i) {
        dataContainers.push(new Currency(symbols[i]))
    }
    return dataContainers;
}


$(document).ready(function () {

    let timeSpan = $("input[name='timespan']:checked").val();
    fillCharts(timeSpan);

    $("input[type='radio']").change(function () {
        timeSpan = $("input[name='timespan']:checked").val();
        if (timeSpan) {
            runFillChart(timeSpan, $(this).attr("class"));
        }
    });
});

function fillCharts(timestamp) {
    Object.keys(exchanges_data).forEach(function (exchange) {
        runFillChart(timestamp, exchange);
    });
}

function runFillChart(timestamp, exchange) {
    let dataContainers = getDataContainers(symbols)
    let title = exchanges_data[exchange].label
    let canvasId = exchange + 'Chart'
    fillChart(timestamp, title, canvasId, exchange, dataContainers)
}


fillChart = function (timeSpan, title, canvasId, exchange, dataContainers) {

    const {interval, date_start} = getStartDate(timeSpan)
    let promises = []

    dataContainers.forEach(function (container) {
        let request = $.ajax({
            method: "GET",
            url: endpoint,
            data: {
                exchange: exchange,
                symbol: container.symbol,
                interval: interval,
                date_start: date_start
            },
            success: function (data) {
                for (let i = 0; i < data.length; i++) {
                    date = new Date(data[i].open_time);
                    container.data.push({'t': date, 'y': Number(data[i].open)});
                    container.labels.push(date.toFormat(interval));
                }
            },
            error: function (error_data) {
                console.log(error_data)
            }
        });
        promises.push(request);
    });

    $.when.apply(null, promises).done(function () {
        drawChart(dataContainers, title, canvasId);
    })
}

drawChart = function (dataContainers, title, canvasId) {
    if (canvasId in charts) {
        charts[canvasId].destroy()
    }
    let ctx = document.getElementById(canvasId).getContext('2d');
    ctx.clearRect(0, 0, ctx.width, ctx.height);
    let datasets = []
    for (let i = 0; i < dataContainers.length; ++i) {
        datasets.push({
            data: dataContainers[i].data,
            label: dataContainers[i].symbol,
            fill: false,
            borderWidth: 2,
            pointStyle: 'line',
            hidden: i !== 0,
            borderColor: colors[i]
        })
    }
    let chart = (new Chart(ctx, {
        type: 'line',
        data: {
            labels: dataContainers[0].labels,
            datasets: datasets
        },
        options: {
            title: {
                display: true,
                text: title,
                fontColor: 'whitesmoke',
                fontSize: 20
            },
            legend: {
                labels: {
                    fontColor: 'whitesmoke',
                    fontSize: 15
                }
            },
            scales: {
                xAxes: [{
                    ticks: {
                        callback: function (tick, index, array) {
                            return (index % 4) ? "" : tick;
                        },
                        fontColor: 'whitesmoke'
                    }
                }],
                yAxes: [{
                    ticks: {
                        fontColor: 'whitesmoke'
                    }
                }]
            }
        }
    }));
    document.getElementById(canvasId).style.visibility = "visible";
    charts[canvasId] = chart
}

function getStartDate(timeSpan) {
    let interval, date_start;
    switch (timeSpan) {
        case '1d':
            interval = "5m";
            date_start = new Date(new Date().setDate(new Date().getDate() - 1)).toUTCString();
            break;
        case '1w':
            interval = "1h";
            date_start = new Date(new Date().setDate(new Date().getDate() - 7)).toUTCString();
            break;
        case '6m':
            interval = "1d";
            date_start = new Date(new Date().setMonth(new Date().getMonth() - 6)).toUTCString();
            break;
        case 'y':
            interval = "1d";
            date_start = new Date(new Date().setFullYear(new Date().getFullYear() - 1)).toUTCString();
            break;
    }
    return {interval, date_start};
}

Date.prototype.toFormat = function (interval) {

    let month_names = ["Jan", "Feb", "Mar",
        "Apr", "May", "Jun",
        "Jul", "Aug", "Sep",
        "Oct", "Nov", "Dec"];

    let day = this.getDate();
    let month_index = this.getMonth();
    let year = this.getFullYear();

    let hour = this.getHours();
    let minutes = this.getMinutes();
    minutes = (minutes < 10 ? "0" : "") + minutes;
    let timeOfDay = (hour < 12) ? "AM" : "PM";

    let str = "";

    switch (interval) {
        case "5m":
            str = "" + hour + ":" + minutes + " " + timeOfDay;
            break;
        case "1h":
            str = "" + hour + ":" + minutes + " " + timeOfDay + " " + day + " " + month_names[month_index];
            break;
        default:
            str = "" + day + " " + month_names[month_index] + " " + year;

    }

    return str;
}