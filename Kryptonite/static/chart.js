const binanceEndpoint = '/api/data/binance';
const poloniexEndpoint = '/api/data/poloniex';

const colors = ['rgba(255, 0, 0, 0.6)', 'rgba(44, 130, 201, 1)', 'rgba(245, 229, 27, 1)', 'rgba(54, 215, 183, 1)']
var charts = [];

class Currency {
    data = []
    labels = []

    constructor(symbol, label) {
        this.symbol = symbol
        this.label = label
    }
}

const binanceSymbols = [['BTCUSDT', 'BTC'], ['ETHUSDT', 'ETH'], ['LTCUSDT', 'LTC'], ['BNBUSDT', 'BNB']];
const poloniexSymbols = [['USDT_BTC', 'BTC'], ['USDT_ETH', 'ETH'], ['USDT_LTC', 'LTC']];

getDataContainers = function (symbols) {
    let dataContainers = []
    for (let i = 0; i < symbols.length; ++i) {
        dataContainers.push(new Currency(symbols[i][0], symbols[i][1]))
    }
    return dataContainers;
}


$(document).ready(function () {

    let timeSpan = $("input[name='timespan']:checked").val();
    fillCharts(timeSpan);

    $("input[type='radio']").change(function () {
        timeSpan = $("input[name='timespan']:checked").val();
        if (timeSpan) {
            fillCharts(timeSpan);
        }
    });
});

function fillBinanceChart(timeSpan) {
    let dataContainers = getDataContainers(binanceSymbols)
    fillChart(timeSpan, 'Binance', 'binanceChart', binanceEndpoint, dataContainers)
}

function fillPoloniexChart(timestamp) {
    let dataContainers = getDataContainers(poloniexSymbols)
    fillChart(timestamp, 'Poloniex', 'poloniexChart', poloniexEndpoint, dataContainers)
}

function fillCharts(timestamp) {
    fillBinanceChart(timestamp)
    fillPoloniexChart(timestamp)
}

fillChart = function (timeSpan, title, canvasId, endpoint, dataContainers) {

    const {interval, date_start} = getStartDate(timeSpan)
    let promises = []

    dataContainers.forEach(function (container) {
        let request = $.ajax({
            method: "GET",
            url: endpoint,
            data: {
                symbol: container.symbol,
                interval: interval,
                date_start: date_start
            },
            success: function (data) {
                for (let i = 0; i < data.length; i++) {
                    container.data.push(Number(data[i].open));
                    date = new Date(data[i].open_time);
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
    destroyCharts()
    let ctx = document.getElementById(canvasId).getContext('2d');
    ctx.clearRect(0, 0, ctx.width, ctx.height);
    let datasets = []
    for (let i = 0; i < dataContainers.length; ++i) {
        datasets.push({
            data: dataContainers[i].data,
            label: dataContainers[i].label,
            fill: false,
            borderWidth: 2,
            pointStyle: 'line',
            hidden: i !== 0,
            borderColor: colors[i]
        })
    }
    charts.push(new Chart(ctx, {
        type: 'line',
        data: {
            labels: dataContainers[0].labels,
            datasets: datasets
        },
        options: {
            title: {
                display: true,
                text: title,
                fontColor: 'rgba(0, 0, 0, 0.6)',
                fontSize: 20
            },
            legend: {
                labels: {
                    fontColor: 'rgb(255, 99, 132)',
                    fontSize: 15
                }
            },
            scales: {
                xAxes: [{
                    ticks: {
                        callback: function (tick, index, array) {
                            return (index % 4) ? "" : tick;
                        }
                    }
                }]
            }
        }
    }));
    document.getElementById(canvasId).style.visibility = "visible";
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

function destroyCharts() {
    if (charts.length === 2) {
        charts.forEach(chart => chart.destroy())
        charts = []
    }
}