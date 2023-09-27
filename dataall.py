import pandas as pd
import os

# Define a function to process a single CSV file
def process_csv(file_path):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_path, sep=';', quoting=3)  # 'quoting=3' handles the quotes around the datetime strings

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

    return df

# Directory containing the CSV files
csv_directory = './csv'

# List all CSV files in the directory
csv_files = [os.path.join(csv_directory, file) for file in os.listdir(csv_directory) if file.endswith('.csv')]

# Process each CSV file and store the results in a dictionary
result_dict = {}
for csv_file in csv_files:
    df = process_csv(csv_file)
    file_name = os.path.basename(csv_file)
    result_dict[file_name] = df

# Now, result_dict contains DataFrames for each CSV file
# You can access them using the file names as keys, e.g., result_dict['btc-hist.csv']
