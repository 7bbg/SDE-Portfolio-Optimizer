import numpy as np

def optimal_stopping_rule(asset_paths, threshold=0.1):
    """
    asset_paths: Simulated asset price paths over time
    threshold: Minimum price change percentage to trigger a rebalance or exit
    """
    decision_points = []
    
    for path in asset_paths:
    
        for t in range(1, len(path)):
            if isinstance(path[t], np.ndarray):
                # If path[t] is an array (multiple assets), compare each asset price change
                price_change_percentage = np.max(np.abs((path[t] - path[t - 1]) / path[t - 1]))  # Take the maximum price change across assets
                
            else:
                # If path[t] is scalar, just compare the price change for that asset
                price_change_percentage = abs((path[t] - path[t - 1]) / path[t - 1])
            
            if price_change_percentage > threshold:
                decision_points.append((t, path[t]))  # Store the time and price at which to stop/rebalance
                break  # Stop or rebalance at this point [Todo: remove for multiple decision points]

    return decision_points
