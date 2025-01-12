import numpy as np
from scipy.optimize import minimize

# Portfolio performance metrics: return and volatility (risk)
def portfolio_performance(weights, mu, sigma, correlation_matrix, risk_tolerance = None):
    """
    Calculate the portfolio performance metrics (return and volatility).
    
    Args:
    - weights: Portfolio weights for each asset.
    - mu: Expected returns for each asset.
    - sigma: Standard deviations of asset returns.
    - correlation_matrix: Correlation matrix between asset returns.
    - risk_tolerance: Risk tolerance factor (higher values indicate more risk taken for higher return).
    
    Returns:
    - portfolio_return: Expected portfolio return.
    - portfolio_volatility: Expected portfolio volatility (risk).
    """
    
    # Calculate the portfolio return (weighted sum of individual asset returns)
    portfolio_return = np.dot(weights, mu)
    
    # Calculate the portfolio volatility (standard deviation of the portfolio)
    portfolio_variance = np.dot(weights.T, np.dot(correlation_matrix * np.outer(sigma, sigma), weights))
    portfolio_volatility = np.sqrt(portfolio_variance)
    
    # Objective function to minimize: Risk-adjusted return (maximize return for given risk tolerance)
    if(risk_tolerance):
        return float(portfolio_volatility - risk_tolerance * portfolio_return)
    
    return portfolio_return, portfolio_volatility



# Optimization function: minimize portfolio volatility for a given return
def optimize_portfolio(mu, sigma, correlation_matrix, risk_tolerance, target_return=None):
    """
    Optimizes the portfolio using Mean-Variance Optimization.
    Returns the optimal portfolio weights, the expected return, and volatility.
    
    Args:
    - mu: mean of daily returns
    - sigma: standard deviation of returns
    - correlation_matrix: correlation matrix of the returns
    - risk_tolerance (float): The investor's risk tolerance, where higher values prefer higher returns over risk.
    - target_return (float): The desired target return for the portfolio.

    Returns:
    - result.x: The optimal portfolio weights.
    - portfolio_return: The expected return for the optimal portfolio.
    - portfolio_volatility: The volatility (risk) for the optimal portfolio.
    """
    num_assets = len(mu)
    
    # Initial guess for portfolio weights (equal allocation)
    initial_weights = np.ones(num_assets) / num_assets
    
    # Bounds for portfolio weights (between 0 and 1)
    bounds = tuple((0, 1) for asset in range(num_assets))
    
    # Constraint to ensure the sum of portfolio weights equals 1
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    
    # If target return is given, we add a constraint for that
    if target_return:
        constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1},
                       {'type': 'eq', 'fun': lambda x: np.dot(x, mu) - target_return})
    
    # Minimize portfolio volatility (risk)
    result = minimize(lambda w: portfolio_performance(w, mu, sigma, correlation_matrix,risk_tolerance),
                      initial_weights,
                      method='SLSQP',
                      bounds=bounds,
                      constraints=constraints)
    
    return result.x, portfolio_performance(result.x, mu, sigma, correlation_matrix)

