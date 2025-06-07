import yfinance as yf
from datetime import datetime

ticker = 'NVDA'
start_date = '2022-01-01'
end_date = datetime.today().strftime('%Y-%m-%d')

df = yf.download(ticker, start=start_date, end=end_date)
df = df.stack(level=1).reset_index()
df.head(10)