import pandas as pd
import numpy as np
from scipy.optimize import minimize
d=["BAJAJFINSV.NS","BAJFINANCE.NS","SBILIFE.NS","SHRIRAMFIN.NS","HDFCLIFE.NS","PFC.NS","RECLTD.NS","CHOLAFIN.NS","ICICIGI.NS","BAJAJHLDNG.NS"]
print(len(d))
import yfinance as yf
import pandas as pd

# Define a list of ticker symbols
ticker_symbols = ["BAJAJFINSV.NS", "BAJFINANCE.NS", "SBILIFE.NS", "SHRIRAMFIN.NS", "HDFCLIFE.NS", "PFC.NS", "RECLTD.NS",
                  "CHOLAFIN.NS", "ICICIGI.NS", "BAJAJHLDNG.NS"]  # Example list of ticker symbols

# Define the start and end dates
start_date = '2018-01-01'
end_date = '2024-01-01'

# Create an empty DataFrame to store the data
adj_close_df = pd.DataFrame()

# Loop through each ticker symbol
for symbol in ticker_symbols:
    # Fetch monthly data from Yahoo Finance
    data = yf.download(symbol, start=start_date, end=end_date, interval='1mo')

    # Extract adjusted close prices and add to the DataFrame
    adj_close_df[symbol] = data['Adj Close']

# Display the DataFrame
print(adj_close_df)
# Sample data: historical returns for three assets

df = adj_close_df

# Calculate annualized mean returns and covariance matrix
annual_returns = df.mean() * 252  # Assuming 252 trading days per year
cov_matrix = df.cov() * 252        # Annualize covariance matrix

# Define Sharpe Ratio function to be minimized
def neg_sharpe_ratio(weights, returns, cov_matrix, risk_free_rate):
    portfolio_return = np.sum(returns * weights)
    portfolio_std_dev = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
    sharpe_ratio = (portfolio_return - risk_free_rate) / portfolio_std_dev
    return -sharpe_ratio

# Constraints for optimization: sum of weights = 1
constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})

# Bounds for weights: between 0 and 1
bounds = tuple((0, 1) for _ in range(len(df.columns)))

# Initial guess for weights
initial_guess = np.array([1.0 / len(df.columns) for _ in range(len(df.columns))])

# Risk-free rate (assumed)
risk_free_rate = 0.05

# Perform optimization
result = minimize(neg_sharpe_ratio, initial_guess, args=(annual_returns, cov_matrix, risk_free_rate),
                  method='SLSQP', bounds=bounds, constraints=constraints)

# Extract optimized weights
optimized_weights = result.x
print("Optimized Portfolio Weights:")
for i, asset in enumerate(df.columns):
    print(asset + ": " + str(round(optimized_weights[i], 4)))

# Calculate and print optimized portfolio metrics
optimized_portfolio_return = np.sum(annual_returns * optimized_weights)
optimized_portfolio_std_dev = np.sqrt(np.dot(optimized_weights.T, np.dot(cov_matrix, optimized_weights)))
optimized_sharpe_ratio = (optimized_portfolio_return - risk_free_rate) / optimized_portfolio_std_dev

print("\nOptimized Portfolio Metrics:")
print("Expected Return:", round(optimized_portfolio_return, 4))
print("Standard Deviation:", round(optimized_portfolio_std_dev, 4))
print("Sharpe Ratio:", round(optimized_sharpe_ratio,4))
