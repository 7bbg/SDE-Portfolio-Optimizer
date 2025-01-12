import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import unittest
from unittest.mock import patch
import numpy as np
import matplotlib.pyplot as plt
from src.efficient_frontier import plot_effifient_frontier  
from src.portfolio_optimizer import optimize_portfolio  

class TestPlotEfficientFrontier(unittest.TestCase):

    @patch('src.portfolio_optimizer.optimize_portfolio')  # Mocking optimize_portfolio
    @patch('matplotlib.pyplot.show')  # Mocking plt.show to prevent actual plotting during tests
    def test_plot_effifient_frontier(self, mock_show, mock_optimize):
        # Sample test data for inputs
        mu_annualized = np.array([0.05, 0.06, 0.07])
        sigma_annualized = np.array([0.1, 0.12, 0.15])
        correlation_matrix = np.array([[1, 0.5, 0.3], [0.5, 1, 0.4], [0.3, 0.4, 1]])
        risk_tolerance = 1.0
        
        # Mocking the output of optimize_portfolio to simulate portfolio optimization
        mock_optimize.return_value = (np.array([0.4, 0.3, 0.3]), (0.06, 0.1))  # Example mock output
        
        # Call the function to plot the efficient frontier
        plot_effifient_frontier(mu_annualized, sigma_annualized, correlation_matrix, risk_tolerance)
        
        
        # Verify that plt.show() was called
        mock_show.assert_called()
        
    
    @patch('src.portfolio_optimizer.optimize_portfolio')  # Mocking optimize_portfolio
    @patch('matplotlib.pyplot.show')  # Mocking plt.show to prevent actual plotting during tests
    def test_invalid_input(self, mock_show, mock_optimize):
        # Empty arrays
        mu_annualized = np.array([])
        sigma_annualized = np.array([])
        correlation_matrix = np.array([[]])
        risk_tolerance = 1.0
        
        # Call the function with invalid input and expect it to handle the error
        with self.assertRaises(ValueError):
            plot_effifient_frontier(mu_annualized, sigma_annualized, correlation_matrix, risk_tolerance)
        
        # Ensure that optimize_portfolio and plt.show are not called with invalid input
        mock_optimize.assert_not_called()
        mock_show.assert_not_called()

if __name__ == '__main__':
    unittest.main()
