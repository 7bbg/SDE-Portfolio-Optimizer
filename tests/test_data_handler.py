import unittest
import numpy as np
import pandas as pd
from unittest.mock import patch
from src.data_handler import fetch_data, get_return, get_correlation_matrix, annualize_parameters

class TestDataProcessing(unittest.TestCase):

    @patch('yfinance.download')
    def test_fetch_data(self, mock_download):

        # Mocking the data returned by yfinance
        mock_data = pd.DataFrame({
            'Adj Close': {
            '2023-01-01': 100,
            '2023-01-02': 105,
            '2023-01-03': 110
            },
            'Asset1': [100, 105, 110],
            'Asset2': [50, 55, 60]
        }, index=pd.to_datetime(['2023-01-01', '2023-01-02', '2023-01-03']))

        mock_download.return_value = mock_data
        
        assets = ['Asset1', 'Asset2']
        data = fetch_data(assets)

        # Check if the downloaded data matches the mocked data
        np.testing.assert_equal(data.values, mock_data['Adj Close'].values)
        
        # Check if the correct file is saved (mocking)
        mock_download.assert_called_once_with(assets, start="2010-01-01", end="2025-01-01", auto_adjust=False, threads=5)
    
    def test_get_return(self):
        raw_data = pd.DataFrame({
            'Asset1': [100, 105, 110],
            'Asset2': [50, 55, 60]
        }, index=pd.to_datetime(['2023-01-01', '2023-01-02', '2023-01-03']))
        
        returns = get_return(raw_data)
        
        # Expected returns calculation
        expected_returns = pd.DataFrame({
            'Asset1': [0.05, 0.047619],
            'Asset2': [0.1, 0.090909]
        }, index=pd.to_datetime(['2023-01-02', '2023-01-03']))
        
        # Test if the returns are calculated correctly
        pd.testing.assert_frame_equal(returns, expected_returns)
    
    def test_get_correlation_matrix(self):
        returns = pd.DataFrame({
            'Asset1': [0.05, 0.04],
            'Asset2': [0.1, 0.08]
        })
        
        # Calculate correlation matrix
        correlation_matrix = get_correlation_matrix(returns)
        

        # Test if the correlation matrix is calculated correctly
        pd.testing.assert_frame_equal(correlation_matrix, returns.corr())
    
    def test_annualize_parameters(self):
        # Sample mean and standard deviation of daily returns
        mu = np.array([0.05, 0.02])
        sigma = np.array([0.1, 0.15])
        
        # Expected results for annualization (252 trading days per year)
        expected_annualized_mu = mu * 252
        expected_annualized_sigma = sigma * np.sqrt(252)
        
        # Call annualize_parameters
        annualized_return, annualized_volatility = annualize_parameters(mu, sigma, 252)
        
        # Test if the annualized returns and volatility are calculated correctly
        np.testing.assert_almost_equal(annualized_return, expected_annualized_mu)
        np.testing.assert_almost_equal(annualized_volatility, expected_annualized_sigma)

if __name__ == '__main__':
    unittest.main()
