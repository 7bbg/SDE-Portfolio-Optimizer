'''
Purpose: Unit tests for the Monte Carlo simulations
'''

import unittest
import pandas as pd
import numpy as np
from src.simulations import simulate_portfolio

class TestMonteCarloSimulation(unittest.TestCase):

    def setUp(self):
        
        self.assets_size = 3  # Number of assets in the portfolio
        self.initial_asset_prices = np.array([100, 150, 200])  # Initial prices of assets
        self.mu_annualized = pd.Series([0.05, 0.07, 0.03], index=['Asset1', 'Asset2', 'Asset3'])  # Expected returns (mu)
        self.sigma_annualized = pd.Series([0.2, 0.3, 0.15], index=['Asset1', 'Asset2', 'Asset3'])  # Volatility (sigma)
        self.time_horizon = 1  # 1 year
        self.time_step = 1/252  # Daily time steps (252 trading days in a year)
        self.n_simulations = 1000  # Number of simulations
        self.n_steps = 252  # Number of time steps (daily steps for 1 year)

    def test_simulate_portfolio_shape(self):
        simulated_prices = simulate_portfolio(
            self.assets_size, self.initial_asset_prices, self.mu_annualized, self.sigma_annualized, 
            self.time_horizon, self.time_step, self.n_simulations, self.n_steps
        )
        # Assert the shape is correct (n_simulations, n_steps, assets_size)
        self.assertEqual(simulated_prices.shape, (self.n_simulations, self.n_steps, self.assets_size))

    def test_simulated_prices_non_zero(self):
        simulated_prices = simulate_portfolio(
            self.assets_size, self.initial_asset_prices, self.mu_annualized, self.sigma_annualized, 
            self.time_horizon, self.time_step, self.n_simulations, self.n_steps
        )
        # Assert that there are no zeros in the simulated prices
        self.assertTrue(np.all(simulated_prices != 0), "Simulated prices should not be all zeros.")

    def test_simulate_portfolio_returns(self):
        simulated_prices = simulate_portfolio(
            self.assets_size, self.initial_asset_prices, self.mu_annualized, self.sigma_annualized, 
            self.time_horizon, self.time_step, self.n_simulations, self.n_steps
        )
        final_prices = simulated_prices[:, -1, :]  # Get the final prices for each simulation
        # Check that the final prices are greater than 0
        self.assertTrue(np.all(final_prices > 0), "Final prices should be positive.")

    def test_simulate_portfolio_returns_shape(self):
        
        simulated_prices = simulate_portfolio(
            self.assets_size, self.initial_asset_prices, self.mu_annualized, self.sigma_annualized, 
            self.time_horizon, self.time_step, self.n_simulations, self.n_steps
        )
        final_prices = simulated_prices[:, -1, :]  # Get the final prices for each simulation

        # Assert the shape is (n_simulations, assets_size)
        self.assertEqual(final_prices.shape, (self.n_simulations, self.assets_size))


if __name__ == '__main__':
    unittest.main()