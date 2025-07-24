import requests
import pandas as pd
import matplotlib.pyplot as plt
import datetime

# Step 1: Fetch Bitcoin data from CoinGecko API (last 30 days)
url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
params = {
    "vs_currency": "usd",
    "days": "30",
    "interval": "daily"
}

response = requests.get(url, params=params)
data = response.json()

# Step 2: Extract date and prices
prices = data['prices']  # [timestamp, price]
df = pd.DataFrame(prices, columns=['Timestamp', 'Price'])

# Convert timestamp to date
df['Date'] = pd.to_datetime(df['Timestamp'], unit='ms')
df.set_index('Date', inplace=True)
df.drop('Timestamp', axis=1, inplace=True)

# Step 3: Calculate daily returns (% change)
df['Daily_Return_%'] = df['Price'].pct_change() * 100

# Step 4: Plotting
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 6), gridspec_kw={'height_ratios': [2, 1]})

# Line plot for Bitcoin Price
ax1.plot(df.index, df['Price'], color='royalblue')
ax1.set_title('Bitcoin price (USD)')
ax1.set_ylabel('Price (USD)')

# Histogram for Daily Returns
ax2.hist(df['Daily_Return_%'].dropna(), bins=20, color='skyblue', edgecolor='black')
ax2.set_title('Distribution of daily returns (%)')
ax2.set_xlabel('Daily % change')
ax2.set_ylabel('Frequency')

plt.tight_layout()
plt.show()
