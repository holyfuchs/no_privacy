let timeSeriesChart = null;

function destroyTimeSeriesGraph() {
    if (timeSeriesChart) {
        timeSeriesChart.destroy();
    }
    document.getElementById('timezoneInfo').innerHTML = "";
}

async function createTimeSeriesGraph(address) {
    const response = await fetch(`/api/time-data/${address}`);
    const timeSeriesData = await response.json();

    // Update timezone info
    document.getElementById('timezoneInfo').innerHTML =
        `<h2>Estimated Time Zone: ${timeSeriesData.timezone}</h2>`;

    // Create or update chart
    const ctx = document.getElementById('timeChart').getContext('2d');
    timeSeriesChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: Array.from({ length: 24 }, (_, i) => `${i}:00`),
            datasets: [{
                label: 'Transaction Count',
                data: timeSeriesData.counts,
                fill: false,
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top'
                },
                title: {
                    display: true,
                    text: `Transaction Activity by Hour (UTC)`
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Number of Transactions'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Hour of Day'
                    }
                }
            }
        }
    });
}