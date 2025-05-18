


// chart


const dateLabels = ["2025-05-01 10:00", "2025-05-01 11:00", "2025-05-01 12:00", "2025-05-01 13:00","2025-05-01 10:00", "2025-05-01 11:00", "2025-05-01 12:00", "2025-05-01 13:00"];
const temperatureValues = [22.5, 23.1, 24.0, 25.3,22.5, 23.1, 24.0, 25.3];

const ctx = document.getElementById('Charttemperature').getContext('2d');
const myCharttemperature = new Chart(ctx, {
    type: 'line',
    data: {
        labels: dateLabels,
        datasets: [{
            label: 'Temperature',
            data: temperatureValues,
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 2
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false, // ← ważne dla pełnego wypełnienia kontenera
    }
});


