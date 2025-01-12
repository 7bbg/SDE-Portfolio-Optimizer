"""
Purpose: Unit tests to ensure the correctness of portfolio optimization logic.
"""
import unittest
from src.portfolio_optimizer import optimize_portfolio, portfolio_performance
import pandas as pd
import numpy as np
from scipy.optimize import minimize

class TestPortfolioOptimization(unittest.TestCase):

    def setUp(self):
        # Sample data for testing: Expected returns (mu), standard deviations (sigma), and correlation matrix
        self.mu = np.array([0.05, 0.07, 0.06])  # Sample expected returns for 3 assets
        self.sigma = np.array([0.1, 0.2, 0.15])  # Sample standard deviations for 3 assets
        self.correlation_matrix = np.array([
            [1.0, 0.5, 0.3],
            [0.5, 1.0, 0.4],
            [0.3, 0.4, 1.0]
        ])  # Correlation matrix between the assets
        self.risk_tolerance = 0.5  # Example risk tolerance

    def test_portfolio_performance(self):
        # Test portfolio performance for a specific set of weights
        weights = np.array([0.4, 0.4, 0.2])  # Portfolio weights
        expected_return = np.dot(weights, self.mu) 
        
        # Portfolio volatility calculation (standard deviation)
        portfolio_variance = np.dot(weights.T, np.dot(self.correlation_matrix * np.outer(self.sigma, self.sigma), weights))
        expected_volatility = np.sqrt(portfolio_variance)
        
        # Call the portfolio_performance function to get the actual performance
        portfolio_return, portfolio_volatility = portfolio_performance(weights, self.mu, self.sigma, self.correlation_matrix)

        # Assert if the return and volatility are calculated correctly
        self.assertAlmostEqual(portfolio_return, expected_return, places=4)
        self.assertAlmostEqual(portfolio_volatility, expected_volatility, places=4)
    
    def test_portfolio_performance_with_risk_tolerance(self):
        # Test portfolio performance with risk tolerance
        weights = np.array([0.4, 0.4, 0.2]) 
        # We expect the result to include risk tolerance affecting the objective function.
        performance_with_risk = portfolio_performance(weights, self.mu, self.sigma, self.correlation_matrix, self.risk_tolerance)
        
        # Since the function returns risk-adjusted return, check if it's greater than 0 
        self.assertGreater(performance_with_risk, 0)

    def test_optimize_portfolio(self):
        # Test optimization without target return 
        optimal_weights, (portfolio_return, portfolio_volatility) = optimize_portfolio(self.mu, self.sigma, self.correlation_matrix, self.risk_tolerance)
        
        # Check if the optimization returned valid weights
        self.assertEqual(len(optimal_weights), len(self.mu))  # Number of assets in portfolio
        self.assertTrue(np.isclose(np.sum(optimal_weights), 1))  # Weights must sum to 1

        # Check if the return and volatility are expected values
        self.assertGreater(portfolio_return, 0)  # Expected return should be positive
        self.assertGreater(portfolio_volatility, 0)  # Expected volatility should be positive
    
    def test_optimize_portfolio_with_target_return(self):
        # Test optimization with a target return
        target_return = 0.06
        optimal_weights, (portfolio_return, portfolio_volatility) = optimize_portfolio(self.mu, self.sigma, self.correlation_matrix, self.risk_tolerance, target_return=target_return)
        
        # Check if the target return constraint is met
        self.assertTrue(np.isclose(np.dot(optimal_weights, self.mu), target_return, atol=1e-2))  # Dot product should be close to target return
        self.assertEqual(len(optimal_weights), len(self.mu))  # Number of assets in portfolio
        self.assertTrue(np.isclose(np.sum(optimal_weights), 1))  # Weights must sum to 1

        # Check if the return and volatility are expected values
        self.assertGreater(portfolio_return, 0)  # Expected return should be positive
        self.assertGreater(portfolio_volatility, 0)  # Expected volatility should be positive
    

if __name__ == '__main__':
    unittest.main()
