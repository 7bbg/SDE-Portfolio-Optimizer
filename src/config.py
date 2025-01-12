# user-defined parameters for portfolio optimization

# List of selected assets (Tickers)
ASSETS = ['AAPL', 'TSLA', '^IRX']

# Risk tolerance level (1-10, where 10 is highest risk tolerence )
RISK_TOLERANCE = 5

#Time horizon for investment (in years)
TIME_HORIZON = 1

# Rebalancing frequency: 'Yearly', 'Quarterly'
REBALANCING_FREQUENCY = 'Quarterly'

# Investment goal (Growth, Income, etc.)
RETURN_EXPECTATIONS = 0.06,  # 6% annual return

# Risk-free rate (US Treasury bond rate)
RISK_FREE_RATE = 0.02 # 2% risk-free rate
