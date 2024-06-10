#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
from polygon import RESTClient
from concurrent.futures import ThreadPoolExecutor, as_completed
from polygon.exceptions import BadResponse

# Initialize the RESTClient with the provided API key
api_key = ""
client = RESTClient(api_key)

# Load the Excel file
file_path = "/Users/dwijesh/Desktop/ProjectFIles/finalTick.xlsx"
df = pd.read_excel(file_path)

# Function to process each row
def process_row(index, row):
    ticker = row['tick']
    date = row['created_at']
    try:
        response = client.get_daily_open_close_agg(ticker, date)
        if response.open and response.close:
            daily_return = (response.close - response.open) / response.open
        else:
            daily_return = None
    except BadResponse as e:
        print(f"Error for {ticker} on {date}: {e}")
        daily_return = None
    return index, daily_return

# Initialize a list to store the daily returns
daily_returns = [None] * len(df)

# Use ThreadPoolExecutor to make requests concurrently
with ThreadPoolExecutor(max_workers=10) as executor:
    # Submit all tasks to the executor
    futures = {executor.submit(process_row, index, row): index for index, row in df.iterrows()}

    for future in as_completed(futures):
        index, daily_return = future.result()
        daily_returns[index] = daily_return
        print(f"Processed row {index + 1}/{len(df)}: {daily_return}")


df['daily_return'] = daily_returns


df.to_excel(file_path, index=False)

print("Daily returns calculated and saved successfully.")


# In[ ]:


import pandas as pd


file_path = "/Users/dwijesh/Desktop/ProjectFIles/finalTick.xlsx"
df = pd.read_excel(file_path)

num_empty_rows = df['daily_return'].isna().sum()

print(f"Number of empty rows in 'daily_return' column: {num_empty_rows}")


# In[ ]:


import pandas as pd


file_path = "/Users/dwijesh/Desktop/ProjectFIles/finalTick.xlsx"
df = pd.read_excel(file_path)

df['created_at'] = pd.to_datetime(df['created_at'])

df['day_of_week'] = df['created_at'].dt.dayofweek

num_saturdays = (df['day_of_week'] == 5).sum()
num_sundays = (df['day_of_week'] == 6).sum()

print(f"Number of Saturdays: {num_saturdays}")
print(f"Number of Sundays: {num_sundays}")


# In[ ]:


import pandas as pd


file_path = "/Users/dwijesh/Desktop/ProjectFIles/finalTick.xlsx"
df = pd.read_excel(file_path)

df['created_at'] = pd.to_datetime(df['created_at'])

df['day_of_week'] = df['created_at'].dt.dayofweek

weekday_df = df[(df['day_of_week'] != 5) & (df['day_of_week'] != 6)]

num_empty_rows_weekdays = weekday_df['daily_return'].isna().sum()

print(f"Number of empty rows in 'daily_return' column on weekdays but are stock market holidays: {num_empty_rows_weekdays}")


# In[ ]:


import pandas as pd

file_path = "/Users/dwijesh/Desktop/ProjectFIles/finalTick.xlsx"
df = pd.read_excel(file_path)

df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')

df_cleaned = df.dropna(subset=['daily_return'])

if 'day_of_week' in df_cleaned.columns:
    df_cleaned = df_cleaned.drop(columns=['day_of_week'])

# Format the 'created_at' column to remove the time part
df_cleaned['created_at'] = df_cleaned['created_at'].dt.date

output_file_path = "/Users/dwijesh/Desktop/ProjectFIles/finalTick_cleaned.xlsx"
df_cleaned.to_excel(output_file_path, index=False)

print(f"Cleaned data exported to {output_file_path}")

