#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd

# Load the data
file_path = '/Users/dwijesh/Desktop/groq/finalTick_with_ai_emphasis.xlsx'
sheet1_data = pd.read_excel(file_path, sheet_name='Sheet1')

# Create separate dataframes for positive and negative daily returns
positive_returns = sheet1_data[sheet1_data['daily_return'] > 0]
negative_returns = sheet1_data[sheet1_data['daily_return'] <= 0]

# Calculate descriptive statistics for positive returns
positive_stats = positive_returns[['daily_return', 'sentiment_score', 'intensity_score', 'ai_emphasis']].describe()

# Calculate descriptive statistics for negative returns
negative_stats = negative_returns[['daily_return', 'sentiment_score', 'intensity_score', 'ai_emphasis']].describe()

# Display the descriptive statistics
print("Positive Returns Descriptive Statistics:\n", positive_stats)
print("\nNegative Returns Descriptive Statistics:\n", negative_stats)


# In[ ]:


import pandas as pd
import numpy as np

# Function to calculate pairwise correlation
def pwcorr(df, method='pearson'):
    df = df.dropna()._get_numeric_data()
    df_cols = pd.DataFrame(columns=df.columns)
    r = df_cols.transpose().join(df_cols, how='outer')
    
    for r_idx, r_col in enumerate(df.columns):
        for c_idx, c_col in enumerate(df.columns):
            if r_idx > c_idx:
                r.loc[r_col, c_col] = ""
            else:
                corr_test = df[[r_col, c_col]].corr(method=method).iloc[0,1]
                r.loc[r_col, c_col] = round(corr_test, 4)
                
    return r

# Load the data
file_path = '/Users/dwijesh/Desktop/groq/finalTick_with_ai_emphasis.xlsx'
sheet1_data = pd.read_excel(file_path, sheet_name='Sheet1')

# Calculate pairwise correlation for daily returns
daily_returns_corr = pwcorr(sheet1_data[['daily_return', 'sentiment_score', 'intensity_score', 'ai_emphasis']])

# Display the correlation coefficients
print("Daily Returns Pairwise Correlation Coefficients:\n", daily_returns_corr)



# In[ ]:


import pandas as pd
import statsmodels.api as sm

# Load the data
file_path = '/Users/dwijesh/Desktop/groq/finalTick_with_ai_emphasis.xlsx'
data = pd.read_excel(file_path, sheet_name='Sheet1')

# Define the dependent and independent variables
X = data[['sentiment_score', 'intensity_score', 'ai_emphasis']]
y = data['daily_return']

# Add a constant to the independent variables matrix
X = sm.add_constant(X)

# Fit the model
model = sm.OLS(y, X).fit()

# Print the summary
print(model.summary())


# In[ ]:


import pandas as pd
import statsmodels.api as sm

# Load the data
file_path = '/Users/dwijesh/Desktop/groq/finalTick_with_ai_emphasis.xlsx'
data = pd.read_excel(file_path, sheet_name='Sheet1')

# Define the dependent and independent variables
X = data[['sentiment_score', 'intensity_score', 'ai_emphasis']]
y = data['daily_return_encoded']

# Add a constant to the independent variables matrix
X = sm.add_constant(X)

# Fit the logistic regression model
model = sm.Logit(y, X).fit()

# Print the summary
print(model.summary())


# In[ ]:


import pandas as pd
import statsmodels.api as sm

# Load the data
file_path = '/Users/dwijesh/Desktop/groq/finalTick_with_ai_emphasis.xlsx'
data = pd.read_excel(file_path, sheet_name='Sheet1')

# Define the dependent and independent variables
X = data[['sentiment_score', 'intensity_score', 'ai_emphasis']]
y = data['daily_return']

# Add a constant to the independent variables matrix
X = sm.add_constant(X)

# Fit the model
model = sm.OLS(y, X).fit()

# Print the summary
print(model.summary())


# In[ ]:


import pandas as pd
import matplotlib.pyplot as plt

# Load the Excel file
file_path = '/Users/dwijesh/Desktop/groq/finalTick_with_ai_emphasis.xlsx'
data = pd.read_excel(file_path)

# Create a binary variable for daily_return
data['daily_return_encoded'] = (data['daily_return'] > 0).astype(int)

# Count the number of 1s and 0s for each emotion
emotion_counts_simplified = data.groupby(['emotion', 'daily_return_encoded']).size().unstack(fill_value=0)

# Filter to include only the top 10 emotions based on overall counts
top_emotions = emotion_counts_simplified.sum(axis=1).nlargest(10).index
emotion_counts_top_10 = emotion_counts_simplified.loc[top_emotions]

# Plot the number of 1s and 0s for each of the top 10 emotions as a grouped bar graph
emotion_counts_top_10.plot(kind='bar', stacked=False, figsize=(15, 8))
plt.title('Number of Positive (1) and Negative (0) Returns by Top 10 Emotions')
plt.xlabel('Emotion')
plt.ylabel('Count')
plt.legend(title='Daily Return Encoded', labels=['0 (Negative)', '1 (Positive)'])
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

