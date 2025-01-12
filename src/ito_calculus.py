'''
purpose: implements Ito's Lemma and Geometric Brownian Motion (GBM) for modelling asset price dymamics
'''

import numpy as np

# For individual asset
def gbm_sde(S0, mu, sigma, T, dt):
    """
    S0: Initial asset price
    mu: Expected return (drift)
    sigma: Volatility (standard deviation)
    T: Total time in years
    dt: Time step for simulation (e.g., daily = 1/252)
    """
    num_steps = int(T / dt)
    S = np.zeros(num_steps)
    S[0] = S0
    for t in range(1, num_steps):
        dW = np.random.normal(0,1) * np.sqrt(dt)
        dS = mu * S[t - 1] * dt + sigma * S[t - 1] * dW
        S[t] = S[t - 1] + dS

    return S