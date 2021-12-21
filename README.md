# New-York-Times-Headlines-Sentiment-Analyzer
New York Times Headlines Sentiment Analyzer, as the name suggests, analyzes and deciphers the sentiments behind the news headlines. It provides the user to search news articles based upon a particular keyword and also asks the user the number of articles they want to be considered while analyzing the dominant sentiment.

Two significant phases involved New York Times Headlines Sentiment Analyzer are:

**1. Data Collection:** 
The data is collected using the New York Times Article API. New York Times is one of the most reliable and vast sources of news and information; thus - the API  has been chosen. The  New York Times Article API returns data in JSON format, which is pre-processed and converted into a pandas data frame for ease of use.

**2. Sentiment Analysis using TextBlob:** 
Sentiment Analysis refers to determining the dominant emotion behind textual information. Here, we've used TextBlob - NLTK based textual processing library for analyzing the sentiment. The sentiment is identified in terms of polarity (positive, negative, or neutral) and subjectivity

