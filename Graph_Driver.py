#Adam and Bryce's Final Project
import tweepy
from tweepy import OAuthHandler
import re
import time
from PIL import Image
import pickle
import matplotlib.pyplot as plt
import matplotlib
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import yfinance as yf
from datetime import datetime
from textblob import TextBlob
import altair as alt
import streamlit as st

alt.renderers.enable('altair_viewer')

#Open CSV and convert to pandas data frame
myDF = pd.read_csv("elonmusk_tweets.csv",encoding = "ISO-8859-1")



tweetList = myDF['text'].tolist()
dateList = myDF['created_at'].tolist()
dateClean = []
sentiments = []

for tweet in tweetList:
    blob = TextBlob(tweet)
    sentiments.append(blob.sentiment.polarity)

for date in dateList:
    dateClean.append(date[0:10])
dateSent = list(zip(dateClean,sentiments))
i = 0
binnedList = []
while i < (len(dateSent)-1):
    summer = dateSent[i][1]
    divisor = 1
    while(dateSent[i][0] == dateSent[i+1][0]):
        summer = summer + dateSent[i+1][1]
        divisor = divisor+1
        i = i+1
    binnedList.append((dateSent[i][0],summer/divisor))
    i = i+1
dfFI = yf.download('TSLA', start = binnedList[-1][0], end = binnedList[0][0], progress = False)
source = pd.DataFrame(binnedList,columns=['Date','Average_Sentiment'])
source2 = pd.DataFrame({
  'Date': dfFI.index,
  'Price (USD)': dfFI["Adj Close"]
})
bar = alt.Chart(source).mark_bar().encode(
    x=alt.X('Date', axis=alt.Axis(labels=False)),
    y=alt.Y('Average_Sentiment', axis=alt.Axis(labels=True)),
    color=alt.condition(
        alt.datum.Average_Sentiment > 0,
        alt.value("green"),  # The positive color
        alt.value("red")  # The negative color
    )
).properties(width=700, height = 400, title = 'Sentiment of Elon Musk\'s Tweets, and Share Price of TSLA')
line = alt.Chart(source2).mark_line().encode(
    alt.X('Date',axis=alt.Axis(labels=False)),
    alt.Y('Price (USD)',axis=alt.Axis(labels=True))
).properties(width=700, height = 400)
#.properties(width=700, height = 400)
chart = alt.layer(bar, line).resolve_scale(
    y = 'independent',
    x = 'independent'
)


chart.show()

#print(sentiments[0:10])













# with open ('outputBTC.txt', 'rb') as fp:
#     list_1 = pickle.load(fp)
#
# #print(list_1[0][3])
# prices = []
# times = []
# negatives = []
# neutrals = []
# positives = []
# old_value = list_1[0][1]
# old_value2 = list_1[0][0]
#
# for tuple in list_1[0:30]:
#
#     prices.append(tuple[0])
#     #Derivative Lines
#     #prices.append(tuple[0]-old_value2)
#     #positives.append((tuple[1]-old_value))
#
#     times.append(tuple[3])
#     positives.append(tuple[1])
#     negatives.append(tuple[2])
#     neutrals.append(100-(tuple[1]+tuple[2]))
#     old_value = tuple[1]
#     old_value2 = tuple[0]
#
# df = pd.DataFrame(list(zip(positives, negatives, neutrals,times)), columns =['Positive', 'Negative','Neutral','Time'])
# print(df.head)

###MATPLOTLIB TESTS
# dates = matplotlib.dates.date2num(times)
#
# fig, ax1 = plt.subplots()
# color = 'tab:red'
# ax1.set_xlabel('Time')
# ax1.set_ylabel('Share Price USD', color=color)
# ax1.plot(dates, prices, color=color)
# ax1.tick_params(axis='y', labelcolor=color)
#
# ax2 = ax1.twinx()
# color = 'tab:blue'
# ax2.set_ylabel('Tweet Positivity (%)', color=color)
# ax2.plot(dates, positives, color=color)
# ax2.tick_params(axis='y', labelcolor=color)
#
# fig.tight_layout()  # otherwise the right y-label is slightly clipped
# plt.show()

#PLOTLY Experiments
# t = np.linspace(0, 100, len(prices))
#
# fig = px.line(x=t, y=prices, labels={'x':'t', 'y':'Price USD'})
# fig.show()

#fig = px.pie(df, values='Positive', names='country', title='Population of European continent')
# fig = px.pie(df, val animation_frame="year", animation_group="country",
#            size="pop", color="continent", hover_name="country",
#            log_x=True, size_max=55, range_x=[100,100000], range_y=[25,90])
#
# fig["layout"].pop("updatemenus") # optional, drop animation buttons


#Altair Plot of SPY, annotated with key news articles...
# start_date = '2020-02-01'
# end_date = '2020-12-01'
# df2 = yf.download("SPY", start = start_date, end = end_date, progress = False)
# #print(df2.head(5))
#
# source = pd.DataFrame({
#   'Date': df2.index,
#   'Price (USD)': df2["Adj Close"]
# })
#
# source['DateStr'] = source['Date'].dt.strftime('%Y%m%d')
# dateList = source['DateStr'].tolist()
# urlList = []
# for date in dateList:
#     urlList.append('https://www.nytimes.com/search?dropmab=true&endDate='+date+'&query=COVID&sort=best&startDate='+date)
#
# source['URLs'] = urlList
# print(source.head(5))
#
# chart = alt.Chart(source).mark_point().encode(
#     x='Date',
#     y='Price (USD)',
#     tooltip=['DateStr','Price (USD)','URLs'],
#     href='URLs'
# ).interactive()
# chart.show()





#
# ###Figure 1 for SPY
# fig = px.line(df2, x=df2.index, y="Adj Close")
#
# fig.add_annotation(x="2020-02-19", y=333.6,
#             text='Fed Affirms U.S. Economy Strong<br><a href="https://tinyurl.com/yyevhmob">Yahoo! Finance</a>',
#             showarrow=True,
#             arrowhead=1)
#
#
# fig.add_annotation(x="2020-02-27", y=293.6,
#             text='COVID Fears Drive Markets Down<br><a href="https://www.nytimes.com/2020/02/27/business/stock-market-coronavirus.html">New York Times</a>',
#             showarrow=True,
#             arrowhead=1)
#
#
# fig.show()
#
# #Figure 2
# df3 = yf.download("AAPL", start = start_date, end = end_date, progress = False)
# fig = px.line(df3, x=df3.index, y="Adj Close")
#
# # fig.add_annotation(x="2020-02-19", y=333.6,
# #             text='Fed Affirms U.S. Economy Strong<br><a href="https://tinyurl.com/yyevhmob">Yahoo! Finance</a>',
# #             showarrow=True,
# #             arrowhead=1)
#
#
# # fig.add_annotation(x="2020-02-27", y=293.6,
# #             text='COVID Fears Drive Markets Down<br><a href="https://www.nytimes.com/2020/02/27/business/stock-market-coronavirus.html">New York Times</a>',
# #             showarrow=True,
# #             arrowhead=1)
#
#
# fig.show()


#fig.show()
