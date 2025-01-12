'''
Purpose: utility functions for additional calculation ( [1]Sharpe ratio)
'''
def calculate_sharpe_ratio(returns, risk_free_rate=0):
    excess_returns = returns.mean() - risk_free_rate
    return excess_returns / returns.std()