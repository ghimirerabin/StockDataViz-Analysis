import yfinance as yf

# Download stock data
tesla_data = yf.download('TSLA', start='2021-01-01', end='2021-12-31')

# Reset index
tesla_data.reset_index(inplace=True)

# Display first five rows
print(tesla_data.head())
