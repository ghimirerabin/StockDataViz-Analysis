import yfinance as yf

# Fetch historical stock data for GameStop (GME)
gme = yf.Ticker('GME')
gme_data = gme.history(period="max")

# Reset the index of the DataFrame
gme_data.reset_index(inplace=True)

# Display the first five rows of the DataFrame
print(gme_data.head(5))
