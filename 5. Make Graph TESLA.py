import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt

# URL of the webpage containing Tesla's revenue data
tesla_url = "https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue"

# Fetch the HTML content of the webpage
html_data = requests.get(tesla_url).text

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_data, "html5lib")

# Create an empty DataFrame to store Tesla's revenue data
tesla_revenue = pd.DataFrame(columns=["Date", "Revenue"])

# Find the table containing Tesla's revenue data
for table in soup.find_all('table'):
    if table.find('th').getText().startswith("Tesla Quarterly Revenue"):
        # Extract data from each row of the table
        for row in table.find("tbody").find_all("tr"):
            col = row.find_all("td")
            if len(col) != 2:
                continue
            Date = col[0].text
            Revenue = col[1].text.replace("$", "").replace(",", "")
            # Append the extracted data to the DataFrame
            tesla_revenue = tesla_revenue.append({"Date": Date, "Revenue": Revenue}, ignore_index=True)

# Drop NaN and empty string values
tesla_revenue.dropna(axis=0, how='all', inplace=True)
tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""]

# Display the last five rows of the DataFrame
print(tesla_revenue.tail())

# Now, let's fetch the stock data for Tesla using yfinance
import yfinance as yf

# Fetch historical stock data for Tesla
tesla_stock = yf.Ticker('TSLA')
tesla_data = tesla_stock.history(period="max")

# Reset the index of the DataFrame
tesla_data.reset_index(inplace=True)

# Display the first five rows of the DataFrame
print(tesla_data.head())

# Define the make_graph function
def make_graph(stock_data, revenue_data, company_name):
    fig, ax1 = plt.subplots()

    color = 'tab:red'
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Stock Price', color=color)
    ax1.plot(stock_data['Date'], stock_data['Close'], color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()  
    color = 'tab:blue'
    ax2.set_ylabel('Revenue', color=color)
    ax2.plot(revenue_data['Date'], revenue_data['Revenue'], color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()  
    plt.title(f'{company_name} Stock Price and Revenue')
    plt.show()

# Call the make_graph function for Tesla
make_graph(tesla_data, tesla_revenue, 'Tesla')
