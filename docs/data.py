import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# Define ticker and time range
ticker = "RELIANCE.NS"  # Reliance Industries Limited on NSE
end_date = datetime.today()
start_date = end_date - timedelta(days=7)  # 7 days to account for weekends

# Download last 7 days of data
data = yf.download(ticker, start=start_date, end=end_date, interval="1d",multi_level_index=False)

# Get last 5 trading days
last_5_days = data.tail(5)
print(last_5_days)


import yfinance as yf

# Reliance ticker on NSE
ticker = "RELIANCE.NS"

# Create ticker object
reliance = yf.Ticker(ticker)

# Get live price
ltp = reliance.history(period="1d")["Close"].iloc[-1]

print(f"Last Traded Price (LTP) of Reliance: ₹{ltp:.2f}")
