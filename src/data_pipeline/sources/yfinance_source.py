import yfinance as yf
from datetime import datetime

def fetch_stock_market_prices(ticker, start_date, end_date=None):
    if end_date is None:
        end_date = datetime.today().strftime('%Y-%m-%d')
    df = yf.download(ticker, start=start_date, end=end_date, auto_adjust=True)
    df = df.stack(level=1, future_stack=True).reset_index()
    return df
