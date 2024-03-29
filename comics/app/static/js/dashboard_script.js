var ctxbarseries = document.getElementById('SeriesBarChart');
var ctxbarclient = document.getElementById('ClientBarChart');

var SeriesBarChart = new Chart(ctxbarseries, {
    type: 'bar',
    data: {
        labels: JSON.parse(document.getElementById('labels_series_counts').textContent),
        datasets: [{
            label: 'Number of clients subscribed',
            data: JSON.parse(document.getElementById('data_series_counts').textContent),
            backgroundColor: [
                "rgba(255, 99, 132, 0.2)",
                "rgba(54, 162, 235, 0.2)",
                "rgba(255, 206, 86, 0.2)",
                "rgba(75, 192, 192, 0.2)",
                "rgba(153, 102, 255, 0.2)"
            ],
            borderColor: [
                "rgba(255, 99, 132, 1)",
                "rgba(54, 162, 235, 1)",
                "rgba(255, 206, 86, 1)",
                "rgba(75, 192, 192, 1)",
                "rgba(153, 102, 255, 1)",
            ],
            borderWidth: 1,
            barThickness: 20,
        }]
    },
    options: {
        indexAxis: 'y',
        /*maintainAspectRatio: false,
        responsive: false*/
    }
}
);

var ClientBarChart = new Chart(ctxbarclient, {
    type: 'bar',
    data: {
        labels: JSON.parse(document.getElementById('labels_client_counts').textContent),/*frameworks,*/
        datasets: [{
            label: 'Number of clients',
            data: JSON.parse(document.getElementById('data_client_counts').textContent),/*stars,*/
            backgroundColor: [
                "rgba(255, 99, 132, 0.2)",
                "rgba(54, 162, 235, 0.2)",
                "rgba(255, 206, 86, 0.2)",
                "rgba(75, 192, 192, 0.2)",
                "rgba(153, 102, 255, 0.2)"
            ],
            borderColor: [
                "rgba(255, 99, 132, 1)",
                "rgba(54, 162, 235, 1)",
                "rgba(255, 206, 86, 1)",
                "rgba(75, 192, 192, 1)",
                "rgba(153, 102, 255, 1)",
            ],
            borderWidth: 1,
        }]
    },
    options: {
        plugins: {
            legend: {
                display: false,
            }
        }
        /*maintainAspectRatio: false,
        responsive: false*/
    }
}
)

