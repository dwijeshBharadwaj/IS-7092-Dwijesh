#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
from groq import Groq
import time

# Reading the Excel file into a DataFrame
df = pd.read_excel('/Users/dwijesh/Desktop/groq/groqData.xlsx', engine='openpyxl')

# Convert the 'text' column into a list
text_list = df['text'].tolist()

# Initialize the Groq client with the API key
client = Groq(api_key='')

# Initialize an empty list to store the results
results = []

# Define the scale description
scale_description = (
    "I need you to rate this text on a scale from 1 to -1, where:\n"
    "- the text has to be evaluated based on the VADER model,\n"
    "- for each of the text based on the VADER model, you need to provide both sentiment score and intensity score\n"
    "\nYour answer should be two single numbers one for sentiment score of the text and the other for the intensity score of the text and there should be no text in the answer."
)

# Iterate over the text list in batches of 2
for i in range(0, len(text_list), 10):
    batch = text_list[i:i+10]
    
    for text in batch:
        prompt = f"{text}\n\n{scale_description}"
        
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama3-8b-8192",
        )
        
        # Extract the rating from the response
        rating = chat_completion.choices[0].message.content.strip()
        
        # Append the rating to the results list
        results.append(rating)
    
    # Print the results for the current batch
    print(results[-10:])  
    
    # Throttling and timeout
    if i + 2 < len(text_list):  # To avoid unnecessary delay after the last batch
        time.sleep(10)

print(results)


# In[ ]:


df['sentiment'] = results
df.to_excel('/Users/dwijesh/Desktop/groq/df_withSentiment.xlsx', index=False)


# In[ ]:


import pandas as pd
from groq import Groq
import time

# Reading the Excel file into a DataFrame
df = pd.read_excel('/Users/dwijesh/Desktop/groq/finalTick_cleaned_no_multiword.xlsx', engine='openpyxl')

# Convert the 'text' column into a list
text_list = df['text'].tolist()

# Initialize the Groq client with the API key
client = Groq(api_key='')

# Initialize an empty list to store the results
results = []

# Define the scale description for AI emphasis
scale_description = (
    "I need you to rate this text for AI emphasis on a scale from 1 to 5, where below are the points that define the scale:\n"
    "- 1 represents that this text has no mention on Artificial intelligence and the text given does not have a context on  Artificial intelligence \n"
    "- 2 represents that this text has low emphasis on Aritificial intelligence ,\n"
    "- 3 represents moderate emphasis on Aritificial intelligence and there is a context in the text,\n"
    "- 4 represents high emphasis and the texts is talking about the Aritificial intelligence,\n"
    "- 5 represents very high emphasis that is, the text only has a specific context on Aritificial intelligence.\n"
    "\nYour answer should be a single digit number and there should be no text in the answer."

)

# Iterate over the text list in batches of 10
for i in range(0, len(text_list), 12):
    batch = text_list[i:i+12]
    batch_number = (i // 12) + 1
    print(f"Processing batch {batch_number}...")
    
    for text in batch:
        try:
            if not text or len(text.split()) < 5:
                results.append('1')
            else:
                prompt = f"{text}\n\n{scale_description}"
                
                chat_completion = client.chat.completions.create(
                    messages=[
                        {
                            "role": "user",
                            "content": prompt,
                        }
                    ],
                    model="llama3-8b-8192",
                )
                
                # Extract the rating from the response
                rating = chat_completion.choices[0].message.content.strip()
                
                # Append the rating to the results list
                results.append(rating)
        
        except Exception as e:
            print(f"An error occurred while processing the text: {text}")
            print(f"Error: {e}")
            results.append('error')
    
    # Print the results for the current batch
    print(f"Results for batch {batch_number}: {results[-12:]}")
    
    # Throttling and timeout
    if i + 12 < len(text_list):  # To avoid unnecessary delay after the last batch
        time.sleep(3)

print("Final results:")
print(results)


# In[ ]:


df['ai_emphasis'] = results

# Saving the DataFrame to a new Excel file
df.to_excel('/Users/dwijesh/Desktop/groq/finalTick_with_ai_emphasis.xlsx', index=False, engine='openpyxl')


# In[ ]:


# Define the new scale description for emotion analysis
scale_description = (
    "I need you to identify the primary emotion expressed in the following text. Your answer should be a one-word response indicating the emotion. Do not include any extra text or explanation."
)

# Initialize an empty list to store the results
results = []

# Iterate over the text list in batches of 10
for i in range(0, len(text_list), 10):
    batch = text_list[i:i+10]
    
    for text in batch:
        prompt = f"{text}\n\n{scale_description}"
        
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama3-8b-8192",
        )
        
        # Extract the emotion from the response
        emotion = chat_completion.choices[0].message.content.strip()
        
        # Append the emotion to the results list
        results.append(emotion)
    
    # Print the results for the current batch
    print(results[-10:])  
    
    # Throttling and timeout
    if i + 10 < len(text_list):  # To avoid unnecessary delay after the last batch
        time.sleep(10)

print(results)

