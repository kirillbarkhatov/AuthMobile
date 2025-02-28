// Получаем данные из атрибута HTML
const chartDataElement = document.getElementById('chart-data');
const attemptSuccessCount = parseInt(chartDataElement.getAttribute('data-success'), 10);
const attemptFailureCount = parseInt(chartDataElement.getAttribute('data-failure'), 10);


const ctx = document.getElementById('myChart').getContext('2d');
const myChart = new Chart(ctx, {
    type: 'bar', // тип графика
    data: {
        labels: ['Успешно', 'Неуспешно'],
        datasets: [{
            label: '# of Votes',
            data: [attemptSuccessCount, attemptFailureCount],
            backgroundColor: [

                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 99, 132, 0.2)'
            ],
            borderColor: [

                'rgba(54, 162, 235, 1)',
                'rgba(255, 99, 132, 1)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});
