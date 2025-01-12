const submitButton = document.getElementById('submit-button');
const riskToleranceInput = document.getElementById('risk-tolerance');
const rebalanceFrequencyInput = document.getElementById('rebalance-frequency');
const timeHorizonInput = document.getElementById('time-horizon');
const assets = document.getElementById("assets");
const returnExpectationInput = document.getElementById('return-expectation')


submitButton.addEventListener('click', () => {
    const riskTolerance = parseFloat(riskToleranceInput.value);
    const rebalanceFrequency = rebalanceFrequencyInput.value;
    const timeHorizon = parseFloat(timeHorizonInput.value);
    const returnExpectation = parseFloat(returnExpectationInput.value);
    const selectedAssets = Array.from(document.getElementById("assets").selectedOptions)
                                .map(option => option.value);
    
    // Note: Send inputs to the backend for portfolio optimization
    if (selectedAssets.length > 0){
        // Note: Disable the button to prevent multiple clicks
        submitButton.disabled = true;

        fetch('http://localhost:5000/optimize', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                risk_tolerance: riskTolerance,
                rebalancing_frequency: rebalanceFrequency,
                time_horizon: timeHorizon,
                assets: selectedAssets,
                return_expectations: returnExpectation,
            }),
        })
        .then((response) => response.json())
        .then((data) => {
            let resultString = " ";
    
            for (let i in data.optimal_weights) {
                resultString += `${selectedAssets[i]} - ${data.optimal_weights[i]} | `;
            }
    
    
            document.getElementById('portfolio-weights').innerText = `Portfolio Weights: |${resultString}`;
            document.getElementById('portfolio-return').innerText = `Portfolio Return: ${data.excepted_return}%`;
            document.getElementById('portfolio-volatility').innerText = `Portfolio Volatility: ${data.portfolio_volatility}%`;
            document.getElementById('portfolio-var').innerText = `Portfolio Value at Risk(VaR): ${data.VaR}`;
        
            // Visualize the data using Chart.js
            const ctx1 = document.getElementById('portfolio-chart1').getContext('2d');
            const ctx2 = document.getElementById('portfolio-chart2').getContext('2d');
    
            // Destroy previous chart instance if it exists
            if (window.chart1 instanceof Chart) {
                window.chart1.destroy();
            }

            window.chart1 = new Chart(ctx1, {
                type: 'line',
                data: {
                    labels: Array.from({ length: data.effifient_frontier.length }, (_, i) => i + 1),
                    datasets: [{
                        label: 'Efficient Frontier',
                        data: data.effifient_frontier,
                        borderColor: 'rgb(28, 26, 167)',
                        backgroundColor: 'rgba(75, 192, 192, 0.2)',
                        fill: true, 
                        tension: 0.1, 
                    }]
                },
                options: {
                    scales: {
                        x: {
                            title: {
                                display: true,
                                text: 'Volatility (Risk)'
                            }
                        },
                        y: {
                            title: {
                                display: true,
                                text: 'Expected Return'
                            }
                        }
                    }
                }
                });
            const trading_days_in_year = 252;

            const roundToOneDecimal = (num) => {
                return Math.round(num * 10) / 10;
            
            };
            const timeLabels = Array.from({ length: data.simulation_portfolio_values[0].length }, (_, i) => `Year ${roundToOneDecimal(i/trading_days_in_year)}`);
            
            const colorPalette = [
                '#FF5733', // Red
                '#33FF57', // Green
                '#3357FF', // Blue
                '#FF33A8', // Pink
                '#F0E130', // Yellow
                '#8E44AD', // Purple
                '#E74C3C', // Coral
                '#16A085', // Teal
                '#F39C12', // Orange
                '#2ECC71'  // Emerald
          ];
          
            const datasets =  data.simulation_portfolio_values.map((path, index) => ({
                label: `Path ${index + 1}`,
                data: path,
                fill: false,
                borderColor: colorPalette[index % colorPalette.length],
                backgroundColor: `${colorPalette[index % colorPalette.length]}80`,
                tension: 0.1,
            }));
            const config = {
                type: 'line',
                data: {
                labels: timeLabels,
                datasets: datasets,
                },
                options: {
                responsive: true,
                scales: {
                    x: {
                    title: {
                        display: true,
                        text: 'Time (Years)',
                    },
                    Max: 252,
                    },
                    y: {
                    title: {
                        display: true,
                        text: 'Portfolio Value',
                    },
                    min: 0,
                    },
                },
                },
            };
            // Destroy previous chart instance if it exists
            if (window.chart2 instanceof Chart) {
                window.chart2.destroy();
            }
            window.chart2 = new Chart(ctx2, config);
        })
        .catch((error) => console.error('Error:', error)).finally(() => {
            // Note:  Re-enable the button after the request is complete
            submitButton.disabled = false;
        });
    } else {
        console.error("No Assets Selected");
    }
    
});
