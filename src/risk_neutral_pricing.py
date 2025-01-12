'''
purpose: implement Risk-Neutral Pricing for derivative options
'''

from scipy.stats import norm
import numpy as np


def risk_neutral_price(S0, K, T, r, sigma, option_type='call'):
    """
    Calculate the risk-neutral price of a European option using Black-Scholes model.
    
    S0: Initial asset price
    K: Strike price
    T: Time to maturity in years
    r: Risk-free interest rate
    sigma: Volatility of the underlying asset
    option_type: "call" or "put"
    """
    
    # Error handling for invalid input
    if S0 <= 0 or K <= 0 or T <= 0 or r < 0 or sigma <= 0:
        raise ValueError("All input parameters must be positive, with sigma and time to maturity > 0.")
    
    if option_type not in ['call', 'put']:
        raise ValueError("option_type must be either 'call' or 'put'.")

    # Calculate d1 and d2 for the Black-Scholes formula
    d1 = (np.log(S0 / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    # Calculate price based on option type
    if option_type == 'call':
        price = (S0 * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2))
    elif option_type == 'put':
        price = (K * np.exp(-r * T) * norm.cdf(-d2) - S0 * norm.cdf(-d1))
    
    return price