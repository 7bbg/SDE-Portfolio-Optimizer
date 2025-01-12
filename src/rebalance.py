'''
Purpose: Rebalance portfolio weights at specified interval (quarterly, yearly, or others).
'''

import numpy as np
import time
from portfolio_optimizer import optimize_portfolio
from optimal_stopping import optimal_stopping_rule

def continuous_monitoring_and_rebalancing(data, risk_tolerance, rebalance_frequency='quarterly', threshold=0.03):
    print("Continuous monitoring and rebalancing started\n")
    
    # Calculate daily returns
    returns = data.pct_change(fill_method=None).dropna()
    
    # Annualize expected returns and volatilities
    mu = returns.mean() * 252  # Annualized expected returns
    sigma = returns.std() * np.sqrt(252)  # Annualized volatilities
    
    # Calculate correlation matrix
    correlation_matrix = returns.corr()
    
    # Initial portfolio weights
    optimal_weights, (initial_return, initial_volatility) = optimize_portfolio(mu.values, sigma.values, correlation_matrix, risk_tolerance)
    
    # Set the rebalance period
    rebalance_periods = {'Quarterly': 63, 'Yearly': 252}  

    for i in range(0, len(data), rebalance_periods[rebalance_frequency]):
        # Extract the data up to the current point
        data_slice = data.iloc[:i + rebalance_periods[rebalance_frequency]]
        returns_slice = data_slice.pct_change(fill_method=None).dropna()
        
        # Recalculate expected returns and volatilities based on the latest data slice [Todo: Use data_handler]
        mu_new = returns_slice.mean() * 252
        sigma_new = returns_slice.std() * np.sqrt(252)
        correlation_matrix_new = returns_slice.corr()
        
        # Optimize portfolio based on the new data
        new_optimal_weights, (new_return, new_volatility) = optimize_portfolio(mu_new.values, sigma_new.values, correlation_matrix_new, risk_tolerance)
        
        # Integrate optimal stopping rule (decision points) here to check for significant price changes
        decision_points = optimal_stopping_rule(data_slice.values, threshold)
        
        if decision_points:
            for dp in decision_points:
                t, price = dp
                print(f"Decision point triggered at day {i+t}. Significant price change detected: {price}")
                # Rebalance portfolio based on decision points
                new_optimal_weights = adjust_weights_based_on_price_change(new_optimal_weights, price)
        
        # Print portfolio details after rebalancing
        print(f"Rebalancing at day {i + rebalance_periods[rebalance_frequency]}")
        print(f"New Portfolio Weights: {new_optimal_weights}")
        print(f"New Portfolio Return: {new_return * 100:.2f}%")
        print(f"New Portfolio Volatility: {new_volatility * 100:.2f}%\n")
        

        time.sleep(1)  # Simulate the passage of time [Todo: If using daily time remove]

def adjust_weights_based_on_price_change(new_optimal_weights, price, threshold=0.03):
    """
    Adjust portfolio weights based on significant price changes.
    new_optimal_weights: Current portfolio weights
    price: The current price of the asset
    threshold: The percentage change in price to trigger a weight adjustment
    """
    adjusted_weights = new_optimal_weights.copy()
    
    # Calculate price change percentage from previous value
    price_change_percentage = (price - adjusted_weights) / adjusted_weights
    
    # Iterate through each price change percentage and adjust portfolio weights if any exceed the threshold
    for i, price_change in enumerate(price_change_percentage):
        if abs(price_change) > threshold:
            if price_change > 0:
                # Reduce weight for assets with significant positive price change (take profits)
                adjusted_weights[i] *= (1 - threshold)
            else:
                # Increase weight for assets with significant negative price change (buy)
                adjusted_weights[i] *= (1 + threshold)

    # Normalize the weights so they sum to 1
    adjusted_weights /= adjusted_weights.sum()

    return adjusted_weights