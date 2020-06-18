const arbitrage_endpoint = '/arbitrage'
const results_data = JSON.parse(document.getElementById('results_data').textContent);
let chart_data = []
results_data.forEach(function (result) {
    let date = new Date(result["time"]);
    date.setHours(date.getHours() - 2);
    chart_data.push({
        "x": date,
        "y": result["profit_rate"]
    })
})

$(document).ready(function () {
    $(function () {
        $('form').on('submit', function (e) {
            $('body').append('<div id="loading"></div>')
            Swal.fire({
                title: 'Running arbitrage',
                html: 'Loading data, it might take a while.',
                allowOutsideClick: false,
                onBeforeOpen: () => {
                    Swal.showLoading()
                }
            })
        });

    })
    let canvas = document.getElementById("resultsChart");
    let ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, ctx.width, ctx.height);
    let chart = new Chart(ctx, {
        type: 'line',
        data: {
            datasets: [{
                data: chart_data,
                showLine: false,
                pointRadius: 12,
                radius: 12,
                pointHoverRadius: 15,
                borderWidth: 4,
                pointBackgroundColor: '#173306',
                pointBorderColor: "#07581b",
            }]
        },
        options: {
            legend: {
                onHover: function (e) {
                    e.target.style.cursor = 'pointer';
                },
                display: false
            },
            hover: {
                onHover: function (e) {
                    var point = this.getElementAtEvent(e);
                    if (point.length) e.target.style.cursor = 'pointer';
                    else e.target.style.cursor = 'default';
                }
            },
            title: {
                display: true,
                text: "Last week opportunities",
                fontColor: 'whitesmoke',
                fontSize: 20
            },
            scales: {
                xAxes: [{
                    type: 'time',
                    time: {
                        unit: 'day'
                    },
                    ticks: {
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
    });
    let originalShowTooltip = chart.showTooltip;
    chart.showTooltip = function (activeElements) {
        $("#dc_LoadTime").css("cursor", activeElements.length ? "pointer" : "default");
        originalShowTooltip.apply(this, arguments);
    }

    canvas.onclick = function (evt) {
        evt.preventDefault()
        const activePoint = chart.getElementAtEvent(evt);
        const datasetIndex = activePoint[0]._datasetIndex;
        const itemIndex = activePoint[0]._index;
        const dataset = chart.data.datasets[datasetIndex];
        const data = dataset.data[itemIndex]
        let time = new Date(data.x)
        time.setHours(time.getHours() + 2)
        console.log(time.toUTCString())
        window.location = '/arbitrage?time=' + time.toUTCString();
    }

    canvas.style.visibility = "visible";
});