"""
Purpose: Entry point
"""
import numpy as np
import yfinance as yf
from matplotlib import pyplot as plt
from data_handler import annualize_parameters, fetch_data, get_return,get_correlation_matrix
from portfolio_optimizer import optimize_portfolio
from rebalance import continuous_monitoring_and_rebalancing
from simulations import simulate_portfolio, simulation_value
from ito_calculus import gbm_sde
from optimal_stopping import optimal_stopping_rule
from risk_neutral_pricing import risk_neutral_price
from efficient_frontier import plot_effifient_frontier
from config import ASSETS, RISK_TOLERANCE, TIME_HORIZON, RETURN_EXPECTATIONS, REBALANCING_FREQUENCY
from utils import calculate_sharpe_ratio



def main():
    trading_days_per_year = 252

    # Fetch and process data
    data = fetch_data(ASSETS)

    returns = get_return(data)

    # Estimate the expected return (mean of daily returns) and volatility (std of returns)
    mu = returns.mean()
    sigma = returns.std()

    # Annualize the parameters (assuming 252 trading days per year)
    mu_annualized, sigma_annualized = annualize_parameters(mu, sigma, trading_days_per_year)

    # Calculate the correlation matrix of the returns
    correlation_matrix = get_correlation_matrix(returns)


    optimal_weights, (expected_return, portfolio_volatility) = optimize_portfolio(mu_annualized.values, sigma_annualized.values, correlation_matrix, RISK_TOLERANCE/10, RETURN_EXPECTATIONS)

    

    # Initial asset prices (last observed price for each asset)
    S0 = data.iloc[-1].values
    dt = 1/252  # Time step (daily data)
    N = 252  # Number of time steps (252 for one year)

    # Simualate portfolio performance
    simulated_path_prices = simulate_portfolio(len(ASSETS), S0, mu_annualized, sigma_annualized, TIME_HORIZON, dt)

    # Simualate portfolio values
    simulation_portfolio_values = simulation_value(size_assets=len(ASSETS), simulated_paths_prices=simulated_path_prices, time_horizon=TIME_HORIZON, plot=True)
    
    # Calculate expected portfolio returns (mean of portfolio values)
    simulation_expected_return = np.mean(simulation_portfolio_values[:, -1]) - 1  # Final value - initial value

    # Calculate portfolio risk (variance of portfolio values)
    simulation_portfolio_risk = np.std(simulation_portfolio_values[:, -1])

    
    # Print the results
    print("\n\n------------------Result------------------")
    print("Annualized Expected Returns (μ):\n", mu_annualized)
    print("\nAnnualized Volatilities (σ):\n", sigma_annualized)
    print("\nCorrelation Matrix:\n", correlation_matrix)
    print(f"\nOptimal Portfolio Weights: {optimal_weights}")
    print(f"\nExpected Portfolio Return: {expected_return * 100:.2f}%")
    print(f"\nPortfolio Volatility: {portfolio_volatility * 100:.2f}%")
    print(f"\nSimulated Expected Portfolio Return: {simulation_expected_return * 100:.2f}%")
    print(f"\nSimulated Portfolio Risk (Standard Deviation): {simulation_portfolio_risk * 100:.2f}%\n")


    # Plot Efficient Frontier
    plot_effifient_frontier(mu_annualized.values, sigma_annualized.values, correlation_matrix, RISK_TOLERANCE/10)

    # Perform Optimal Stopping (e.g, check if rebalancing is needed)
    decision_points = optimal_stopping_rule(simulated_path_prices)

    # print(f"Optimal Stopping Decision Points: {decision_points}") 

    continuous_monitoring_and_rebalancing(data,RISK_TOLERANCE/10, rebalance_frequency= REBALANCING_FREQUENCY)

    for i in range(len(ASSETS)-1): # Note: First 2 select for stock expect bonds or commodities
        # Retrieve the stock data
        asset = yf.Ticker(ASSETS[i])

        # Get the current stock price
        current_price = asset.history(period="1d")['Close'].iloc[0]

        # Get the available expiration dates for options
        expiration_dates = asset.options

        # Choose the first one
        chosen_expiration_date = expiration_dates[0]

        # Get the options chain for the chosen expiration date
        options_chain = asset.option_chain(chosen_expiration_date)

        # Extract the call options data
        calls = options_chain.calls

        # Find the closest strike price to the current stock price
        best_call_strike = calls['strike'].iloc[(calls['strike'] - current_price).abs().argmin()]

        option_price = risk_neutral_price(S0=S0[i], K=best_call_strike, T=TIME_HORIZON, r=0.05, sigma=sigma[ASSETS[i]], option_type="call")
    
        print(f"Option Price for {ASSETS[i]}(Note: Risk-Nuetral): {option_price}")
    


    sharpe_ratio = calculate_sharpe_ratio(returns, sigma)
    print(f"\nSharpe Ratio: {sharpe_ratio}\n")

    for asset in ASSETS:
        # Verify data for each asset
        last_row = data[asset].tail(1)
        # Extract the initial price from the last row
        initial_price = last_row.values[0]

        # Generate asset price paths using GBM
        temp = gbm_sde(S0=initial_price, mu=mu_annualized[asset], sigma=sigma_annualized[asset], T=TIME_HORIZON, dt=dt)
        print(f"Simulated price paths for {asset}:")
        print(temp)



    
if __name__ == "__main__":
    main()
