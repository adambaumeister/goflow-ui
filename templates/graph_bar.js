<script>
var ctx = document.getElementById('{{ c.name }}').getContext('2d');
var chart = new Chart(ctx, {
    // The type of chart we want to create
    type: 'bar',

    // The data for our dataset
    data: {
        labels: [{{ c.labels|safe }} ],
        datasets: [{
            label: "{{ c.name }}",
            backgroundColor: 'rgb(255, 99, 132)',
            borderColor: 'rgb(255, 99, 132)',
            data: [{{ c.data }}],
        }]
    },

    // Configuration options go here
    options: {
        responsive:true,
        maintainAspectRatio: false,
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero:true
                }
            }]
        }
    }
});
$(document).ready( function () {
    var data = chart.data.datasets[0].data
    $("#KBytes").click(function() {
        var newData = []
        $.each(data, function ( index, value ) {
            newData.push(value / 1000)
        });
        chart.data.datasets[0].data = newData;
        chart.update();
    });

    $("#MBytes").click(function() {
        var newData = []
        $.each(data, function ( index, value ) {
            newData.push(value / 1000000)
        });
        chart.data.datasets[0].data = newData;
        chart.update();
    });
});
</script>
<div class="form-container">
    <input type="button" value="KBytes" id="KBytes">
    <input type="button" value="MBytes" id="MBytes">
</div>