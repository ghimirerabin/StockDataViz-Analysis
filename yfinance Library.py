import yfinance as yf
import os

# Define the path to the folder
folder_path = r'C:\Users\Rabin Ghimire\Desktop\Coursera\Python Project for Data Science'

# Check if the folder exists, if not, create it
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

# Download historical data for MSFT
msft = yf.Ticker("MSFT")
msft_data = msft.history(period="max")

# Save the downloaded data to a CSV file in the specified folder
file_path = os.path.join(folder_path, 'MSFT_data.csv')
msft_data.to_csv(file_path

print("Data downloaded and saved successfully at:", file_path)
