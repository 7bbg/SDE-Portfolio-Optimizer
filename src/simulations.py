'''
Purpose: Implement Monte Carlo simulations to simulate future assets price paths
'''
import numpy as np
import matplotlib.pyplot as plt

def simulation_value(size_assets, simulated_paths_prices,time_horizon, n_simulations=1000, n_steps=252, plot=False):
    
    # Initial portfolio weights (equal allocation for each asset)
    portfolio_weights = np.array([1/size_assets] * size_assets)

    # Simulate portfolio values for each path
    portfolio_values = np.zeros((n_simulations, n_steps))

    # Calculate the portfolio value at each time step for each simulated path
    for i in range(n_simulations):
        portfolio_values[i, 0] = 1  # Initial portfolio value (normalized to 1)
        for t in range(1, n_steps):
            # Portfolio value is the weighted sum of the asset prices at time t
            portfolio_values[i, t] = np.sum(portfolio_weights * simulated_paths_prices[i, t, :]) / np.sum(portfolio_weights * simulated_paths_prices[i, 0, :])

    if(plot): 
        # Plot portfolio values over time (for a few paths)
        plt.figure(figsize=(10, 6))
        for i in range(10):  # Plotting first 10 portfolio values
            plt.plot(np.linspace(0, time_horizon, n_steps), portfolio_values[i, :], label=f"Path {i+1}")
        plt.title("Simulated Portfolio Values Over Time")
        plt.xlabel("Time (Years)")
        plt.ylabel("Portfolio Value")
        plt.show()

    return portfolio_values[:10]

def simulate_portfolio(assets_size, initial_asset_prices, mu_annualized, sigma_annualized, time_horizon,  time_step, n_simulations=1000, n_steps=252):
    """
    Simulate multiple price paths for a portfolio of assets using geometric Brownian motion.

    This function generates simulated price paths for each asset over a specified time horizon,
    accounting for the annualized mean returns (`mu_annualized`) and standard deviations (`sigma_annualized`)
    of the assets. The simulation considers correlated random walks (using the Wiener process) and computes
    the price evolution of each asset.

    Parameters:
    - assets_size (int): Number of assets in the portfolio.
    - initial_asset_prices (array): Initial prices of the assets at time t=0.
    - mu_annualized (array): Annualized mean returns for each asset.
    - sigma_annualized (array): Annualized standard deviations (volatility) for each asset.
    - time_horizon (float): Total time horizon for the simulation (in years).
    - time_step (int): Number of time steps per year for the simulation.
    - n_simulations (int, optional): Number of simulations to run (default is 1000).
    - n_steps (int, optional): Number of steps per year (default is 252, assuming daily steps in a year).

    Returns:
    - simulated_prices (array): Simulated asset price paths, with shape (n_simulations, n_steps, assets_size).
    """

    # Simulate the price paths for each asset
    simulated_prices = np.zeros((n_simulations, n_steps, assets_size))

    np.random.seed(42)  # For reproducibility

    for i in range(n_simulations):
        # Simulate correlated random walks for assets
        W = np.random.normal(0, 1, (n_steps, assets_size))  # Standard normal random variables
        W = np.cumsum(W, axis=0) * np.sqrt(time_step)  # Cumulative sum to simulate the Wiener process

        # Calculate assets price paths for each asset
        for j in range(assets_size):
            simulated_prices[i, :, j] = initial_asset_prices[j] * np.exp((mu_annualized.values[j] - 0.5 * sigma_annualized.values[j]**2) * np.linspace(0, time_horizon, n_steps) + sigma_annualized.values[j] * W[:, j])
    
    return simulated_prices