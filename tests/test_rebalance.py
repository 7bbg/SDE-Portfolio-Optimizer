"""
Purpose: Unit tests to verify the rebalacing logic
"""
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import unittest
import numpy as np
import pandas as pd
from src.rebalance import continuous_monitoring_and_rebalancing, adjust_weights_based_on_price_change
from src.portfolio_optimizer import optimize_portfolio  
from src.optimal_stopping import optimal_stopping_rule 

from unittest.mock import patch

class TestContinuousMonitoringAndRebalancing(unittest.TestCase):
    
    def setUp(self):
        # Mock data for asset prices
        self.data = pd.DataFrame({
            'Asset1': [100, 102, 104, 106, 108, 110, 112, 114, 116, 118],  # Increasing price data
            'Asset2': [50, 52, 54, 56, 58, 60, 62, 64, 66, 68],
        }, index=pd.date_range(start='2020-01-01', periods=10, freq='D'))
        
        # Define risk tolerance for testing
        self.risk_tolerance = 0.5
    
    @patch('src.portfolio_optimizer.optimize_portfolio')  # Mocking the optimize_portfolio function
    @patch('src.optimal_stopping.optimal_stopping_rule')  # Mocking the optimal_stopping_rule function
    def test_continuous_monitoring_and_rebalancing(self, mock_optimal_stopping_rule, mock_optimize_portfolio):
        # Mock the return values for optimize_portfolio
        mock_optimize_portfolio.return_value = ([0.6, 0.4], (0.05, 0.1))  # Mock optimal weights and [return/volatility]

        # Mock the return value for optimal_stopping_rule (no significant price changes)
        mock_optimal_stopping_rule.return_value = []
    
        # Run the continuous monitoring and rebalancing function
        with patch('builtins.print') as mock_print:  # Mocking the print statements
            continuous_monitoring_and_rebalancing(self.data, self.risk_tolerance, rebalance_frequency='Quarterly', threshold=0.03)
            
            # Verify that the mock print statements are called 
            mock_print.assert_any_call('Rebalancing at day 63')  # This checks if rebalancing happened on day 63 (quarterly)
            mock_print.assert_any_call('New Portfolio Weights: [0. 1.]')
            
            mock_print.assert_any_call('New Portfolio Return: 875.95%')
            mock_print.assert_any_call('New Portfolio Volatility: 5.26%\n')
    
    @patch('src.portfolio_optimizer.optimize_portfolio')  # Mocking the optimize_portfolio function
    @patch('src.optimal_stopping.optimal_stopping_rule')  # Mocking the optimal_stopping_rule function
    def test_adjust_weights_based_on_price_change(self, mock_optimal_stopping_rule, mock_optimize_portfolio):
        # Mock optimize_portfolio return value
        mock_optimize_portfolio.return_value = ([0.6, 0.4], (0.05, 0.1))  # Mock weights and [return/volatility]
        
        # Sample portfolio weights before price change
        new_optimal_weights = np.array([0.6, 0.4])
        price = np.array([102, 51])  # Simulated price change
        threshold = 0.03
        
        # Adjust portfolio weights based on the simulated price changes
        adjusted_weights = adjust_weights_based_on_price_change(new_optimal_weights, price, threshold)
        
        # Check if the weights were adjusted correctly
        self.assertAlmostEqual(adjusted_weights[0], 0.58, places=1)  # Expecting adjusted weight for Asset 1
        self.assertAlmostEqual(adjusted_weights[1], 0.41, places=1)  # Expecting adjusted weight for Asset 2
    
    @patch('src.portfolio_optimizer.optimize_portfolio')  # Mocking the optimize_portfolio function
    @patch('src.optimal_stopping.optimal_stopping_rule')  # Mocking the optimal_stopping_rule function
    def test_decision_point_triggered(self, mock_optimal_stopping_rule, mock_optimize_portfolio):
        # Mock the return values for optimize_portfolio
        mock_optimize_portfolio.return_value = ([0.6, 0.4], (0.5, 0.1))  # Mock optimal weights and [return/volatility]
        
        # Mock decision points where significant price change is detected
        mock_optimal_stopping_rule.return_value = [(5, 105), (8, 110)]  # Decision points at day 5 and day 8
        

        with patch('builtins.print') as mock_print:
            continuous_monitoring_and_rebalancing(self.data, self.risk_tolerance, rebalance_frequency='Quarterly', threshold=0.03)
        
        # Todo: reform logic

if __name__ == '__main__':
    unittest.main()