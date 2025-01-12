import unittest
import numpy as np
import pandas as pd
from src.utils import calculate_sharpe_ratio

class TestUtilityFunctions(unittest.TestCase):

    def test_calculate_sharpe_ratio(self):
        # Sample returns for testing (daily returns)
        returns = pd.Series([0.01, 0.02, 0.015, 0.03, -0.01]) 
        
        # Assuming a risk-free rate of 0
        risk_free_rate = 0
        
        # Calculate Sharpe ratio
        sharpe_ratio = calculate_sharpe_ratio(returns, risk_free_rate)
        
        # Calculate expected Sharpe ratio
        expected_sharpe_ratio = (returns.mean() - risk_free_rate) / returns.std()

        # Test if the Sharpe ratio is calculated correctly
        self.assertAlmostEqual(sharpe_ratio, expected_sharpe_ratio, places=5)
        
    def test_calculate_sharpe_ratio_with_nonzero_risk_free_rate(self):
        # Sample returns for testing (daily returns)
        returns = pd.Series([0.01, 0.02, 0.015, 0.03, -0.01])  
        
        # Assume a non-zero risk-free rate (0.005 daily)
        risk_free_rate = 0.005
        
        # Calculate Sharpe ratio
        sharpe_ratio = calculate_sharpe_ratio(returns, risk_free_rate)
        
        
        # Calculate expected Sharpe ratio manually
        expected_sharpe_ratio = (returns.mean() - risk_free_rate) / returns.std()
        
        # Test if the Sharpe ratio is calculated correctly
        self.assertAlmostEqual(sharpe_ratio, expected_sharpe_ratio, places=5)
    
    def test_calculate_sharpe_ratio_zero_returns(self):
        # Returns are all zero (no variation)
        returns = pd.Series([0, 0, 0, 0, 0])
        
        # Calculate Sharpe ratio
        sharpe_ratio = calculate_sharpe_ratio(returns)

        # Sharpe ratio should be NaN 
        self.assertTrue(np.isnan(sharpe_ratio))

if __name__ == '__main__':
    unittest.main()
