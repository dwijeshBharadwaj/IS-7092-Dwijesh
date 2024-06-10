#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import requests
import pandas as pd

# Hard-code the bearer token
bearer_token = ''

# Endpoint URL
url = "https://api.twitter.com/2/users/by"

# Load the Excel file and get the list of usernames
handle_df = pd.read_excel('/Users/dwijesh/Desktop/ProjectFiles/twitterHandles.xlsx')
ceo_list = handle_df['CeoHandle'].tolist()

# Define the headers with the bearer token for authentication
headers = {
    'Authorization': f'Bearer {bearer_token}'
}

# Dictionary to store JSON responses
user_details = {}

# Iterate over the list of usernames
for username in ceo_list:
    params = {
        'usernames': username,
        'user.fields': 'id'
    }
    response = requests.get(url, headers=headers, params=params)

    # Check for a successful response
    if response.status_code == 200:
        user_details[username] = response.json()
    else:
        print(f"Failed to retrieve details for {username}: {response.status_code}")
        print(response.text)

# Print the dictionary containing the JSON responses
print(user_details)


# In[ ]:


handle_df['Name'] = handle_df['CeoHandle'].apply(lambda x: user_details[x]['data'][0]['name'] if x in user_details else None)
handle_df['ID'] = handle_df['CeoHandle'].apply(lambda x: user_details[x]['data'][0]['id'] if x in user_details else None)

# Define the path where the Excel file will be saved
file_path = '/Users/dwijesh/Desktop/ProjectFiles/twitterHandles_with_details.xlsx'

# Save the DataFrame to an Excel file without the index
handle_df.to_excel(file_path, index=False)

# Display the DataFrame
handle_id = handle_df['ID'].to_list()
handle_id


# In[ ]:


import requests
import json
from datetime import datetime, timedelta
import pandas as pd
import os

# Hard-code the bearer token
bearer_token = ''

# Define the user ID
user_id = "14773334"

# Define the endpoint
url = f"https://api.twitter.com/2/users/{user_id}/tweets"

# Calculate the start and end times for the past six months
end_time = datetime.utcnow()
start_time = end_time - timedelta(days=365)

# Format the dates in RFC3339 format with milliseconds
end_time_str = end_time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
start_time_str = start_time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

# Parameters for the initial request
params = {
    'max_results': 100,
    'start_time': start_time_str,
    'end_time': end_time_str,
    'tweet.fields': 'created_at,text',
    'expansions': 'author_id',
    'user.fields': 'username'
}

# Define the headers with the bearer token for authentication
headers = {
    'Authorization': f'Bearer {bearer_token}'
}

all_tweets = []
user_info = {}

while True:
    # Make the request to the Twitter API
    response = requests.get(url, headers=headers, params=params)

    # Check for a successful response
    if response.status_code == 200:
        # Parse the JSON response
        tweets = response.json()
        all_tweets.extend(tweets.get('data', []))

        # Extract user information
        if 'includes' in tweets and 'users' in tweets['includes']:
            for user in tweets['includes']['users']:
                user_info[user['id']] = user['username']

        # Check if there is a next_token for pagination
        next_token = tweets.get('meta', {}).get('next_token')
        if next_token:
            params['pagination_token'] = next_token
        else:
            break  
    else:
        print(f"Failed to retrieve tweets: {response.status_code}")
        print(response.text)
        break

# Merge tweet data with user info
for tweet in all_tweets:
    tweet['username'] = user_info.get(tweet['author_id'], 'Unknown')

# Convert the list of tweets to a DataFrame
new_df = pd.DataFrame(all_tweets)

# Define the path for the XLSX file
file_path = '/Users/dwijesh/Desktop/ProjectFiles/omega2.xlsx'

# Check if the file already exists
if os.path.exists(file_path):
    # Read the existing data
    existing_df = pd.read_excel(file_path)
    # Append the new data to the existing data
    combined_df = pd.concat([existing_df, new_df], ignore_index=True)
else:
    # If the file doesn't exist, use the new data as the combined data
    combined_df = new_df

# Save the combined DataFrame to an XLSX file
combined_df.to_excel(file_path, index=False)

if response.status_code == 200:
    print(f"Tweets saved to {file_path}")
else:
    print(response)


# In[ ]:


import pandas as pd
import re
import emoji

def clean_text(text):
    # Remove URLs
    text = re.sub(r'http\S+', '', text)
    
    # Remove emojis
    text = emoji.replace_emoji(text, replace='')
    
    # Remove @mentions, #hashtags, and other symbols
    text = re.sub(r'[@#]\w+', '', text)
    
    # Remove non-alphanumeric characters except spaces
    text = re.sub(r'[^A-Za-z0-9\s]', '', text)
    
    # Remove "RT"
    text = re.sub(r'\bRT\b', '', text)
    
    return text.strip()

# Load the Excel file
file_path = '/Users/dwijesh/Desktop/ProjectFiles/omega2.xlsx'
data_df = pd.read_excel(file_path, engine='openpyxl')

# Remove the 'edit_history_tweet_ids' and 'id' columns
columns_to_remove = ['edit_history_tweet_ids', 'id']
data_df = data_df.drop(columns=[col for col in columns_to_remove if col in data_df.columns])

# Keep only the first 10 characters in the 'created_at' column
if 'created_at' in data_df.columns:
    data_df['created_at'] = data_df['created_at'].astype(str).str[:10]

# Clean the text data in the 'text' column
if 'text' in data_df.columns:
    data_df['text'] = data_df['text'].apply(clean_text)

# Save the modified DataFrame back to the Excel file
output_path = '/Users/dwijesh/Desktop/ProjectFiles/omega2_cleaned.xlsx'
data_df.to_excel(output_path, index=False)

print(f"Cleaned file saved to {output_path}")


# In[ ]:


import pandas as pd

# Load the cleaned Excel file
cleaned_file_path = '/Users/dwijesh/Desktop/ProjectFiles/omega2_cleaned.xlsx'
cleaned_df = pd.read_excel(cleaned_file_path, engine='openpyxl')

# Check for empty rows (if you still want to display them)
empty_rows = cleaned_df[cleaned_df.isnull().any(axis=1)]

# Drop the empty rows
cleaned_df = cleaned_df.dropna()

# Save the cleaned DataFrame back to an Excel file
output_file_path = '/Users/dwijesh/Desktop/ProjectFiles/omega2_cleaned_no_empty_rows.xlsx'
cleaned_df.to_excel(output_file_path, index=False)
print(f"The cleaned DataFrame has been saved to: {output_file_path}")

