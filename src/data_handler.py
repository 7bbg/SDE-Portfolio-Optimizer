'''
Purpose: Fetches and processes historical data, calculates returns, volatility, and correlation

'''

import yfinance as yf
import pandas as pd
import numpy as np
import os

def fetch_data(assets, end_date='2025-01-01'):
    data_folder_path = 'data'

    # Download historical adjusted close prices from yfinace
    data = yf.download(assets, start="2010-01-01", end=end_date, threads=5, auto_adjust=False)['Adj Close'] # Todo: Change end date
    data.to_csv(os.path.join(data_folder_path, 'raw_data.csv'))
    return data

def get_return(raw_data):
    """
    Return calculated daily returns
    
    Args:
    - raw_data: A historical adjusted close prices
    """
    return raw_data.pct_change(fill_method=None).dropna()

def get_correlation_matrix(returns):
    """
    Return correlation matrix of the returns
    
    Args:
    - returns: daily returns for each assets
    """
    return returns.corr()

def annualize_parameters(mu, sigma, trading_days_per_year):
    """
    Return annualize the parameters
    
    Args:
    - mu: mean of daily returns
    - sigma: standard deviation of returns
    - trading_days_per_year: assumed trading days per year

    Returns:
    - Expected return per year
    - Annualized volatility
    """
    return (mu * trading_days_per_year) , sigma * np.sqrt(trading_days_per_year) 