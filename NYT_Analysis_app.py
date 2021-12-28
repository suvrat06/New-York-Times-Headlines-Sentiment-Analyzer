#importing the necessary libraries
import json
import time
from pandas.core.frame import DataFrame
import requests
import pandas as pd
from textblob import TextBlob
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

#Frontend using streamlit
st.title("New York Times Headline Sentiment Analyzer")
st.subheader("News Data Collection and Sentiment Analysis made simple!")
st.write("Hey! Just type down any topic the news headlines of which you'd like to analyze using the sidebar. The sentiment report will be displayed right here.")
st.sidebar.header("Welcome!")
topic=st.sidebar.text_input("What topic you want to search the NYT for?")
number=st.sidebar.slider("How mady articles do you want the analysis to be performed?",10,1000,step=10)

#defining a function to send request and fetch data from New York Time API 
def send_request(query,page_no):
  api_key='E7gUndRRat2yUnLMn1tccCjf7dSJpTY7'
  # https://api.nytimes.com/svc/search/v2/articlesearch.json?q=election&api-key=yourkey
  base_url = 'https://api.nytimes.com/svc/search/v2/articlesearch'
  url = base_url + '.json?q=' + query +'&page='+str(page_no)+ '&api-key=' + api_key
  response=(requests.get(url).json())
  time.sleep(6)
  return response

#querying the API to fetch the data
query=topic
n=number
page=int(n/10)
df=pd.DataFrame()
for i in range(0,page):
  res=send_request(query,i)['response']['docs']
  df=df.append(pd.DataFrame(res))
df.index=[i for i in range(0,n)]
#print(df.head())

#define a function that performs sentiment analysis using textblob
def sentiment_analysis(text):
  return TextBlob(text).sentiment.subjectivity, TextBlob(text).sentiment.polarity

#generating the sentiment report
sentiment_table=pd.DataFrame(columns=['Headline No.','Headline','Polarity','Subjectivity'])
net_polarity=0
net_subjectivity=0
for i in range(0,n):
  sentiment_report=sentiment_analysis(df['headline'][i]['main'])
  new_row=[df['headline'][i]['main'],sentiment_report[1],sentiment_report[0]]
  sentiment_table = sentiment_table.append({'Headline No.': int(i+1), 'Headline' : df['headline'][i]['main'], 'Polarity' : sentiment_report[1], 'Subjectivity' : sentiment_report[0]}, ignore_index = True)
  net_subjectivity=net_subjectivity+sentiment_report[0]
  net_polarity=net_polarity+sentiment_report[1]

mean_subjectivity=net_subjectivity/n
mean_polarity=net_polarity/n

if mean_polarity>0:
  outlook="Positive"
elif mean_polarity<0:
  outlook="Negative"
else:
  outlook="Neutral"

st.subheader("Sentiment Report:")
st.write("The NYT Analyzer just fetched the top ", n, "article headlines on", query, "from the vast New York Times archives and here's the sentiment report!")
st.write("Dominant Outlook: ",outlook)
st.write("Mean Polarity: ", mean_polarity)
st.write("Mean Subjectivity: ",mean_subjectivity)
st.subheader("Analysis Results:")
st.dataframe(sentiment_table)
st.subheader("Individual Headlines Polarity Plot:")
#Visualizing the individual headline sentiments on a bar chart
# fig=sns.barplot(x = 'Headline No.',
#             y = 'Polarity',
#             data = sentiment_table,
#             palette = "Blues")
#sns.set(rc = {'figure.figsize':(15,8)})
#fig=plt.show()
fig = plt.figure(figsize = (10, 5))
plt.bar(sentiment_table["Headline No."], sentiment_table['Polarity'])
plt.xticks(range(1,n+1))
plt.xlabel("Headline No.")
plt.ylabel("Polarity")
plt.title("Headline No. Vs Polarity")
st.pyplot(fig)
