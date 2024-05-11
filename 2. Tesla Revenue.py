import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the webpage containing the revenue data
url = "https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue"

# Fetch the HTML content of the webpage
html_data = requests.get(url).text

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_data, "html.parser")

# Create an empty DataFrame to store the revenue data
tesla_revenue = pd.DataFrame(columns=["Date", "Revenue"])

# Find the table containing the revenue data
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
tesla_revenue.dropna(axis=0, how='all', subset=['Revenue'], inplace=True)
tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""]

# Display the last five rows of the DataFrame
print(tesla_revenue.tail(5))
