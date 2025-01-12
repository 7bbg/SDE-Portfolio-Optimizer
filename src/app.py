# app.py (Flask API)

import numpy as np
from flask import Flask, request, jsonify
app = Flask(__name__)

from data_handler import annualize_parameters, fetch_data, get_return,get_correlation_matrix
from portfolio_optimizer import optimize_portfolio
from simulations import simulate_portfolio, simulation_value
from risk_neutral_pricing import risk_neutral_price
from efficient_frontier import plot_effifient_frontier
from config import ASSETS, RISK_TOLERANCE, TIME_HORIZON, RETURN_EXPECTATIONS, REBALANCING_FREQUENCY

def portfolio(assets=ASSETS, risk_tolerance=RISK_TOLERANCE, time_horizon=TIME_HORIZON, return_expectations=RETURN_EXPECTATIONS,
            rebalancing_frequency=REBALANCING_FREQUENCY):
    trading_days_per_year = 252
    
    # Fetch and process data
    data = fetch_data(assets)

    returns = get_return(data)

    # Estimate the expected return (mean of daily returns) and volatility (std of returns)
    mu = returns.mean()
    sigma = returns.std()

    # Annualize the parameters
    mu_annualized, sigma_annualized = annualize_parameters(mu, sigma, trading_days_per_year)

    # Calculate the correlation matrix of the returns
    correlation_matrix = get_correlation_matrix(returns)


    optimal_weights, (expected_return, portfolio_volatility) = optimize_portfolio(mu_annualized.values, sigma_annualized.values, correlation_matrix, 
                                                                                  risk_tolerance/10,target_return=return_expectations )
    
    S0 = data.iloc[-1].values # last observed price for each asset
    dt = 1/252  # Time step (daily data)

    # Simualate portfolio performance
    simulated_path_prices = simulate_portfolio(len(ASSETS), S0, mu_annualized, sigma_annualized, time_horizon, dt)

    # Simualate portfolio values
    simulation_portfolio_values = simulation_value(size_assets=len(ASSETS), simulated_paths_prices=simulated_path_prices, time_horizon=time_horizon)
    
    # Get just Efficient Frontier data
    effcient_frontier = plot_effifient_frontier(mu_annualized.values, sigma_annualized.values, correlation_matrix, risk_tolerance/10, plot=False)

    # Calculate portfolio VaR (95% confidence interval) using historical simulation
    portfolio_returns = returns.dot(optimal_weights)

    VaR_95 = np.percentile(portfolio_returns, 5)

    
    return optimal_weights.tolist(), str(f'{expected_return * 100:.2f}'), str(f'{portfolio_volatility * 100:.2f}'), str(f'{VaR_95 * 100:.2f}'), effcient_frontier, simulation_portfolio_values

    # Backtesting
    # continuous_monitoring_and_rebalancing(data,risk_tolerance/10, rebalance_frequency= REBALANCING_FREQUENCY)


@app.route('/optimize', methods=['POST'])
def optimize():

    # Get inputs
    data = request.get_json()

    assets =  data['assets']
    risk_tolerance = data['risk_tolerance']
    time_horizon = data['time_horizon']
    return_expectations = data['return_expectations']
    rebalancing_frequency = data['rebalancing_frequency']

    # Call portfolio optimization function
    optimal_weights, excepted_return, portfolio_volatility, VaR, effifient_frontier, simulation_portfolio_values = portfolio(
        assets=assets, risk_tolerance=risk_tolerance, time_horizon=time_horizon, return_expectations=return_expectations, rebalancing_frequency=rebalancing_frequency
    )

    print(simulation_portfolio_values)

    if isinstance(effifient_frontier, np.ndarray):
        effifient_frontier = effifient_frontier.tolist()

    if isinstance(simulation_portfolio_values, np.ndarray):
        simulation_portfolio_values = simulation_portfolio_values.tolist()

    return jsonify({
        'optimal_weights': optimal_weights,
        'excepted_return': excepted_return,
        'portfolio_volatility': portfolio_volatility,
        'VaR': VaR,
        'effifient_frontier': effifient_frontier,
        'simulation_portfolio_values': simulation_portfolio_values,
    })

if __name__ == '__main__':
    app.run(debug=True)
