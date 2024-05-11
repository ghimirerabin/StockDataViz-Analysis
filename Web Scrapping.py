import requests
from bs4 import BeautifulSoup

# Download the contents of the web page
url = "http://www.ibm.com"
data = requests.get(url).text

# Create a BeautifulSoup object
soup = BeautifulSoup(data, "html.parser")

# Scrape all links
for link in soup.find_all('a', href=True):
    print(link.get('href'))

# Scrape all image tags
for link in soup.find_all('img'):
    print(link)
    print(link.get('src'))

# Scrape data from HTML tables
url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DA0321EN-SkillsNetwork/labs/datasets/HTMLColorCodes.html"
data = requests.get(url).text
soup = BeautifulSoup(data, "html.parser")
table = soup.find('table')

for row in table.find_all('tr'):
    cols = row.find_all('td')
    color_name = cols[2].string
    color_code = cols[3].string
    print("{} ---> {}".format(color_name, color_code))

# Scrape data from HTML tables into a DataFrame using BeautifulSoup and Pandas
import pandas as pd

url = "https://en.wikipedia.org/wiki/World_population"
data = requests.get(url).text
soup = BeautifulSoup(data, "html.parser")
tables = soup.find_all('table')

for index, table in enumerate(tables):
    if "10 most densely populated countries" in str(table):
        table_index = index

population_data = pd.DataFrame(columns=["Rank", "Country", "Population", "Area", "Density"])

for row in tables[table_index].tbody.find_all("tr"):
    col = row.find_all("td")
    if col != []:
        rank = col[0].text
        country = col[1].text
        population = col[2].text.strip()
        area = col[3].text.strip()
        density = col[4].text.strip()
        population_data = population_data.append({"Rank": rank, "Country": country, "Population": population, "Area": area, "Density": density}, ignore_index=True)

print(population_data)
