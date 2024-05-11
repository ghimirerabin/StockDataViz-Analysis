import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

# Function to fetch revenue data from the provided URL
def fetch_revenue_data(url):
    # Fetch the HTML content of the webpage
    html_data = requests.get(url).text

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_data, "html5lib")

    # Create an empty DataFrame to store revenue data
    revenue_data = pd.DataFrame(columns=["Date", "Revenue"])

    # Find the table containing the revenue data
    for table in soup.find_all('table'):
        if table.find('th').getText().startswith("GameStop Quarterly Revenue"):
            # Extract data from each row of the table
            for row in table.find("tbody").find_all("tr"):
                col = row.find_all("td")
                if len(col) != 2:
                    continue
                Date = col[0].text
                Revenue = col[1].text.replace("$", "").replace(",", "")
                # Append the extracted data to the DataFrame
                revenue_data = revenue_data.append({"Date": Date, "Revenue": Revenue}, ignore_index=True)

    # Drop NaN and empty string values
    revenue_data.dropna(axis=0, how='all', inplace=True)
    revenue_data = revenue_data[revenue_data['Revenue'] != ""]
    
    return revenue_data

# URL of the webpage containing GameStop's revenue data
gme_url = "https://www.macrotrends.net/stocks/charts/GME/gamestop/revenue"

# Fetch GameStop's revenue data
gme_revenue = fetch_revenue_data(gme_url)

# Fetch historical stock data for GameStop (GME)
gme_stock = yf.Ticker('GME')
gme_data = gme_stock.history(period="max")

# Reset the index of the DataFrame
gme_data.reset_index(inplace=True)

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

# Call the make_graph function for GameStop
make_graph(gme_data, gme_revenue, 'GameStop')
