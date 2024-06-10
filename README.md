# IS-7092-Dwijesh
Sentiment analysis of tweets
# CEO Tweets Sentiment Analysis and Financial Performance Prediction

## Project Overview

This project aims to leverage Large Language Models (LLMs) to extract sentiments and features from tweets posted by the official CEO handles of twenty-four publicly listed companies on the NYSE and CBOE. The selected companies are either from the package software industry or listed on NASDAQ. The primary objective is to assess whether the extracted features can predict the financial performance of these companies by discerning patterns that indicate how tweets by CEOs influence the stock market performance of the associated ticker on an intraday basis.

## Project Phases

### Phase 1: Text Extraction
- **Objective:** Extract tweets from CEO handles.
- **Method:** Using the “X” API (Basic plan), tweets were extracted and stored in an Excel file.
- **Tools Used:** Python, Pandas, Jupyter Notebook, “X” API.

### Phase 2: Calculating Daily Returns
- **Objective:** Calculate daily stock returns for the companies based on ticker and date information.
- **Method:** Using Yahoo Finance API (provided by Polygon.io), daily returns were calculated and appended to the dataset.
- **Tools Used:** Python, Pandas, Polygon.io API, Yahoo Finance API.

### Phase 3: Sentiment Analysis
- **Objective:** Analyze the sentiment of the extracted tweets and relate it to the daily stock returns.
- **Method:** Sentiment scores, intensity scores, emotions, and AI emphasis were extracted using Groq's LPU and logistic regression models were applied.
- **Tools Used:** Python, Statsmodels, Scikit-learn, Groq's API.

### Phase 4: Data Analysis
- **Objective:** To analyze the extracted features (sentiment scores, intensity scores, emotions, and AI emphasis) and their relationship with daily stock returns.
- **Method:** Logistic regression models were used to determine the predictive power of each feature on daily stock returns.
- **Results:** Comprehensive analysis of each feature's impact on predicting daily returns.
