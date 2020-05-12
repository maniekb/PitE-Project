var endpoint = '/api/data/'

var BinanceBTC = []
var Labels = []

$(document).ready(function() {
    $.ajax({
        method: "GET",
        url: endpoint,
        success: function(data){
            console.log(data)
            for(var i = 0; i < data.length; i++)
            {
                BinanceBTC.push(Number(data[i].open));
                date = new Date(data[i].open_time);
                Labels.push(date.toShortFormat());
            }
            drawChart();
        },
        error: function(error_data){
        console.log(error_data)
        }
    });
});



drawChart = function() {
    var ctx = document.getElementById('myChart').getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: Labels,
            datasets:[{
                data: BinanceBTC,
                label: "BTC - Binance",
                fill: false,
                borderColor: 'rgba(255, 0, 0, 0.6)',
                hoverBorderColor: 'rgba(255, 0, 0, 0.8)'
            }]
        },     
        options: {
            title: {
                display: true,
                text: 'Historical Data',
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
                        callback: function(tick, index, array) {
                            return (index % 4) ? "" : tick;
                        }
                    }
                }]
            }
        }
    });
}

Date.prototype.toShortFormat = function() {

    var month_names =["Jan","Feb","Mar",
                      "Apr","May","Jun",
                      "Jul","Aug","Sep",
                      "Oct","Nov","Dec"];
    
    var day = this.getDate();
    var month_index = this.getMonth();
    var year = this.getFullYear();
    
    return "" + day + " " + month_names[month_index] + " " + year;
}