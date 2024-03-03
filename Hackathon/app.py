from flask import Flask, render_template, request

app = Flask(__name__)

# Your optimization model code (import statements and model) here ...

# Sample weights for each sector

def optimize_portfolio(ticker_symbols):
    import pandas as pd
    import numpy as np
    from scipy.optimize import minimize
    import yfinance as yf
    import pandas as pd



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


    df = adj_close_df

    # Calculate annualized mean returns and covariance matrix
    annual_returns = df.mean() *12
    cov_matrix = df.cov() * 12  # Annualize covariance matrix

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
    risk_free_rate = 0.23

    # Perform optimization
    result = minimize(neg_sharpe_ratio, initial_guess, args=(annual_returns, cov_matrix, risk_free_rate),
                      method='SLSQP', bounds=bounds, constraints=constraints)

    # Extract optimized weights
    optimized_weights = result.x


    # Calculate and print optimized portfolio metrics
    optimized_portfolio_return = np.sum(annual_returns * optimized_weights)*0.001
    optimized_portfolio_std_dev = np.sqrt(np.sqrt(np.dot(optimized_weights.T, np.dot(cov_matrix, optimized_weights))))
    optimized_sharpe_ratio = (optimized_portfolio_return - risk_free_rate) / optimized_portfolio_std_dev


    return optimized_weights,optimized_portfolio_return,optimized_portfolio_std_dev,optimized_sharpe_ratio


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/calculate_weight', methods=['POST'])
def calculate_weight():
    selected_sector = request.form['sector']
    ticker_symbols = get_tickers_for_sector(selected_sector)

    # Use your optimization model to get the optimized weights and metrics
    optimized_weights, optimized_portfolio_return, optimized_portfolio_std_dev, optimized_sharpe_ratio = optimize_portfolio(ticker_symbols)

    # Get the asset names
    assets = ticker_symbols

    # Convert optimized_weights and assets to lists for passing to the template

    weights_list = optimized_weights.tolist()

    # Pass both the assets and weights to the template
    return render_template('result.html', sector=selected_sector, assets=assets, weights=weights_list,
                           optimized_portfolio_return=optimized_portfolio_return,
                           optimized_portfolio_std_dev=optimized_portfolio_std_dev,
                           optimized_sharpe_ratio=optimized_sharpe_ratio)


def get_tickers_for_sector(sector):
    if sector == "FINTECH":
        return ["BAJAJFINSV.NS", "BAJFINANCE.NS", "SBILIFE.NS", "SHRIRAMFIN.NS", "HDFCLIFE.NS", "PFC.NS",
                      "RECLTD.NS",
                      "CHOLAFIN.NS", "ICICIGI.NS", "BAJAJHLDNG.NS"]
    if sector == "AUTOMOBILE":
        return ["MOTHERSON.NS","TVSMOTOR.NS","M&M.NS","SONACOMS.NS","ASHOKLEY.NS","MARUTI.NS","BAJAJ-AUTO.NS","TIINDIA.NS","MRF.NS","BHARATFORG.NS","EICHERMOT.NS","BALKRISIND.NS","BOSCHLTD.NS"]
    if sector == "METAL":
        return ["HINDALCO.NS",  "JSWSTEEL.NS", "ADANIENT.NS", "VEDL.NS", "JINDALSTEL.NS", "NMDC.NS","APLAPOLLO.NS",
             "SAIL.NS", "NATIONALUM.NS","HINDZINC.NS","RATNAMANI.NS","HINDCOPPER.NS","JSL.NS","WELCORP.NS"]
    if sector == "FMCG":
        return ["ITC.NS", "HINDUNILVR.NS", "VBL.NS", "NESTLEIND.NS", "TATACONSUM.NS", "DABUR.NS", "COLPAL.NS",
             "GODREJCP.NS", "BRITANNIA.NS", "MARICO.NS", "MCDOWELL-N.NS", "PGHH.NS"]
    if sector == "BANKING":
        return ["PNB.NS","SBIN.NS","IDFCFIRSTB.NS","AUBANK.NS","FEDERALBNK.NS","BANDHANBNK.NS","BANKBARODA.NS","INDUSINDBK.NS","HDFCBANK.NS","KOTAKBANK.NS","ICICIBANK.NS","AXISBANK.NS"]


if __name__ == '__main__':
    app.run(debug=True)
