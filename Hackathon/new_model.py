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

    # ... (rest of the code)

    return optimized_weights, optimized_portfolio_return, optimized_portfolio_std_dev, optimized_sharpe_ratio


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
