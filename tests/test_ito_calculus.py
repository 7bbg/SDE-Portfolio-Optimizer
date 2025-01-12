import unittest
import numpy as np
from src.ito_calculus import gbm_sde 

class TestGBM(unittest.TestCase):
    
    def test_output_type(self):
        # Test that the function returns a numpy array
        S0 = 100
        mu = 0.05
        sigma = 0.2
        T = 1
        dt = 1/252  # daily time step
        S = gbm_sde(S0, mu, sigma, T, dt)
        self.assertIsInstance(S, np.ndarray, "The output should be a numpy array.")
    
    def test_initial_value(self):
        # Test that the initial value is correct
        S0 = 100
        mu = 0.05
        sigma = 0.2
        T = 1
        dt = 1/252
        S = gbm_sde(S0, mu, sigma, T, dt)
        self.assertEqual(S[0], S0, f"Initial value should be {S0}.")
    
    def test_price_dynamics(self):
        # Test that the asset price evolves based on the given drift (mu) and volatility (sigma)
        S0 = 100
        mu = 0.05
        sigma = 0.2
        T = 1
        dt = 1/252
        S = gbm_sde(S0, mu, sigma, T, dt)
        
        # Check if price changes between time steps are non-zero and fluctuating
        price_changes = np.diff(S)
        
        # Assert that there are some fluctuations in the price
        self.assertTrue(np.any(price_changes != 0), "Price changes should not be zero.")
        
        # Check that the price does not exceed certain bounds( no negative prices )
        self.assertTrue(np.all(S >= 0), "Asset price should never be negative.")
        
        # Ensure the final price is close to the expected value with some randomness
        expected_mean = S0 * np.exp(mu * T)  # Deterministic model
        expected_std = sigma * S0 * np.sqrt(T)  # Standard deviation of the GBM process

        # Apply 3-sigma rule
        lower_bound = expected_mean - 3 * expected_std 
        upper_bound = expected_mean + 3 * expected_std 
        
        
        # Check that the final price is within the expected range
        self.assertTrue(lower_bound <= S[-1] <= upper_bound,
                        f"Final asset price {S[-1]:.2f} is outside the expected range ({lower_bound:.2f}, {upper_bound:.2f}).")
    
    def test_zero_volatility(self):
        # Test when sigma (volatility) is zero, price should remain constant
        S0 = 100
        mu = 0.05  # Non-zero drift
        sigma = 0.0  # Zero volatility
        T = 1
        dt = 1/252  # Daily time step
        S = gbm_sde(S0, mu, sigma, T, dt)

        # Calculate the expected change based on drift: mu * S0 * dt
        expected_change = mu * S0 * dt
        
        # Check that the change in price is within a small tolerance of the expected change
        change_in_price = np.max(np.abs(np.diff(S)))  # Max absolute price change
        self.assertTrue(change_in_price <= expected_change * 1.1, 
                        f"Price change should be close to drift, but got {change_in_price}.")

    def test_large_time_steps(self):
        # Test with larger time steps (lower resolution)
        S0 = 100
        mu = 0.05
        sigma = 0.2
        T = 1
        dt = 1/52  # weekly time step
        S = gbm_sde(S0, mu, sigma, T, dt)
        
        # Check that the length of the output array corresponds to the time steps
        num_steps = int(T / dt)
        self.assertEqual(len(S), num_steps, f"Number of steps should be {num_steps}.")
    
if __name__ == '__main__':
    unittest.main()
