# from bs4 import BeautifulSoup
# import requests
# import pandas as pd
# import csv 

# # xrp 
# # url = "https://coinmarketcap.com/currencies/xrp/historical-data/"
# # content = requests.get(url).content
# # soup = BeautifulSoup(content,'html.parser')
# # table = soup.find('div', {'class': 'history'})



# # data = [[td.text.strip() for td in tr.findChildren('td')] 
# #         for tr in table.findChildren('tr')] 


# df = pd.read_csv('xrp-hist.csv')
# df.drop(df.index[0], inplace=True) # first row is empty
# df[0] =  pd.to_datetime(df[0]) # date

# for i in range(1,7):
#     df[i] = pd.to_numeric(df[i].str.replace(",","").str.replace("-","")) # some vol is missing and has -

# df.columns = ['Date','Open','High','Low','Close','Volume','Market Cap']


# df.set_index('Date',inplace=True)
# df.sort_index(inplace=True)
import pandas as pd

# Read the CSV file into a DataFrame
df = pd.read_csv('btc-hist.csv', sep=';', quoting=3)  # 'quoting=3' handles the quotes around the datetime strings

# Remove double quotes from datetime columns and convert to datetime objects
datetime_columns = ['timeOpen', 'timeClose', 'timeHigh', 'timeLow', 'timestamp']
for col in datetime_columns:
    df[col] = pd.to_datetime(df[col].str.strip('""'), format='%Y-%m-%dT%H:%M:%S.%fZ')

# Convert other columns to numeric after cleaning
numeric_columns = ['open', 'high', 'low', 'close', 'volume', 'marketCap']
for col in numeric_columns:
    # Explicitly convert the column to string before applying .str accessor
    df[col] = pd.to_numeric(df[col].astype(str).str.replace(",", "").str.replace("-", ""), errors='coerce')

# Rename columns for clarity
df.rename(columns={
    'timeOpen': 'Open Time',
    'timeClose': 'Close Time',
    'timeHigh': 'High Time',
    'timeLow': 'Low Time',
    'open': 'Open',
    'high': 'High',
    'low': 'Low',
    'close': 'Close',
    'volume': 'Volume',
    'marketCap': 'Market Cap',
    'timestamp': 'Timestamp'
}, inplace=True)

# Set 'Open Time' as the index (or choose another suitable index)
df.set_index('Open Time', inplace=True)

# Sort the DataFrame by the index
df.sort_index(inplace=True)

print(df)
