import unittest
import numpy as np
from src.optimal_stopping import optimal_stopping_rule 

class TestOptimalStoppingRule(unittest.TestCase):
    
    def test_single_asset(self):
        # Test with a single asset price path
        asset_paths = [
            [100, 105, 110, 115, 135]  # Prices increase by 5 each time, should trigger at 135
        ]
        threshold = 0.1  # 10% change to trigger a stop/rebalance
        decision_points = optimal_stopping_rule(asset_paths, threshold)
        
        # Assert that the decision point is correct (t=4, price=125)
        self.assertEqual(decision_points, [(4, 135)], "Decision points for single asset path are incorrect.")

    def test_multiple_assets(self):
        # Test with multiple assets
        asset_paths = [
            [np.array([100, 200]), np.array([105, 195]), np.array([110, 190]), np.array([120, 180]), np.array([135, 250])],  # Prices change for both assets
        ]
        threshold = 0.1  # 10% change to trigger a stop/rebalance
        decision_points = optimal_stopping_rule(asset_paths, threshold)
        
        # Assert that decision point is correctly triggered for price changes
        #self.assertListEqual(decision_points[0][0], 4], "Decision points for multiple asset paths are incorrect.")
        np.testing.assert_equal(decision_points[0], (4, np.array([135, 250])), "Decision points for multiple asset paths are incorrect.")

    def test_no_trigger(self):
        # Test case where no price changes exceed the threshold
        asset_paths = [
            [100, 102, 104, 106, 108]  # Changes are below threshold (2% max)
        ]
        threshold = 0.1  # 10% threshold, no price change should trigger a stop/rebalance
        decision_points = optimal_stopping_rule(asset_paths, threshold)
        
        # Assert that no decision points are returned
        self.assertEqual(decision_points, [], "There should be no decision points when price change is below threshold.")

    def test_multiple_decision_points(self):
        # Test case where multiple decision points exist within a multiple asset path
        asset_paths = [
            [100, 115, 105, 120, 150],  # The price changes exceed threshold at multiple points
            [100, 110, 105, 110, 140]
        ]
        threshold = 0.1  # 10% threshold
        decision_points = optimal_stopping_rule(asset_paths, threshold)

        # Assert that decision points are correctly detected at t=1 (115) and t=4 (140)
        self.assertEqual(decision_points, [(1, 115), (4, 140)], "Multiple decision points not detected properly.")
    
    def test_empty_path(self):
        # Test case where the asset path is empty
        asset_paths = []
        threshold = 0.1
        decision_points = optimal_stopping_rule(asset_paths, threshold)
        
        self.assertEqual(decision_points, [], "There should be no decision points for empty asset paths.")

    def test_path_with_non_array_elements(self):
        # Test with paths containing non-array elements to ensure they are handled properly
        asset_paths = [
            [100, 110, 105, 115, 130]  # Single asset path with scalar values
        ]
        threshold = 0.1
        decision_points = optimal_stopping_rule(asset_paths, threshold)
        
        # Assert that the decision point is correctly triggered at t=4 (price 130)
        self.assertEqual(decision_points, [(4, 130)], "Decision points with scalar elements are incorrect.")
    
if __name__ == '__main__':
    unittest.main()
