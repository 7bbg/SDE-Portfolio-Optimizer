import unittest
import numpy as np
from scipy.stats import norm
from src.risk_neutral_pricing import risk_neutral_price

class TestRiskNeutralPricing(unittest.TestCase):
    
    def test_call_option_price(self):
        # Sample parameters for a call option
        S0 = 100   # Initial stock price
        K = 100    # Strike price
        T = 1      # Time to maturity (1 year)
        r = 0.05   # Risk-free rate (5%)
        sigma = 0.2  # Volatility (20%)
        
        # Expected result based on Black-Scholes formula for a call option
        d1 = (np.log(S0 / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        expected_price = (S0 * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2))
        
        # Test if the function's output matches the expected result
        calculated_price = risk_neutral_price(S0, K, T, r, sigma, option_type='call')
        self.assertAlmostEqual(calculated_price, expected_price, places=5)
    
    def test_put_option_price(self):
        # Sample parameters for a put option
        S0 = 100   # Initial stock price
        K = 100    # Strike price
        T = 1      # Time to maturity (1 year)
        r = 0.05   # Risk-free rate (5%)
        sigma = 0.2  # Volatility (20%)
        
        # Expected result based on Black-Scholes formula for a put option
        d1 = (np.log(S0 / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        expected_price = (K * np.exp(-r * T) * norm.cdf(-d2) - S0 * norm.cdf(-d1))
        
        # Test if the function's output matches the expected result
        calculated_price = risk_neutral_price(S0, K, T, r, sigma, option_type='put')
        self.assertAlmostEqual(calculated_price, expected_price, places=5)
    
    def test_invalid_option_type(self):
        # Test invalid option type
        with self.assertRaises(ValueError):
            risk_neutral_price(100, 100, 1, 0.05, 0.2, option_type='invalid')
    
    def test_invalid_input_parameters(self):
        # Test invalid parameters (negative price, volatility, or time)
        with self.assertRaises(ValueError):
            risk_neutral_price(-100, 100, 1, 0.05, 0.2, option_type='call')  # Negative stock price
            
        with self.assertRaises(ValueError):
            risk_neutral_price(100, -100, 1, 0.05, 0.2, option_type='call')  # Negative strike price
            
        with self.assertRaises(ValueError):
            risk_neutral_price(100, 100, -1, 0.05, 0.2, option_type='call')  # Negative time to maturity
            
        with self.assertRaises(ValueError):
            risk_neutral_price(100, 100, 1, -0.05, 0.2, option_type='call')  # Negative risk-free rate
            
        with self.assertRaises(ValueError):
            risk_neutral_price(100, 100, 1, 0.05, -0.2, option_type='call')  # Negative volatility
    
    def test_zero_time_to_maturity(self):
        # Test for the case when time to maturity is 0 (Should throw error T>=0)
        S0 = 100
        K = 100
        T = 0
        r = 0.05
        sigma = 0.2

        with self.assertRaises(ValueError):
            price = risk_neutral_price(S0, K, T, r, sigma, option_type='call')
        

if __name__ == '__main__':
    unittest.main()
