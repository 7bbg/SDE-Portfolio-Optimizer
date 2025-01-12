'''
Purpose: Function to plot the efficient frontier, showing the optimal portfolio risk-return trade-off.
'''
from matplotlib import pyplot as plt
import numpy as np
from portfolio_optimizer import optimize_portfolio

def plot_effifient_frontier(mu_annualized, sigma_annualized, correlation_matrix, risk_tolerance, plot=True):
    # Generate the Efficient Frontier
    target_returns = np.linspace(min(mu_annualized), max(mu_annualized), 100)
    portfolio_volatilities = []

    for target in target_returns:
        optimal_weights, (expected_return, portfolio_volatility) = optimize_portfolio(mu_annualized, sigma_annualized, correlation_matrix, risk_tolerance, target_return=target)
        portfolio_volatilities.append(portfolio_volatility)
    
    if(plot):
        # Plot the Efficient Frontier
        plt.figure(figsize=(10, 6))
        plt.plot(portfolio_volatilities, target_returns, label="Efficient Frontier", color="b")
        plt.title("Efficient Frontier")
        plt.xlabel("Portfolio Volatility (Risk)")
        plt.ylabel("Portfolio Expected Return")
        plt.grid(True)
        plt.show()

    return  portfolio_volatilities
