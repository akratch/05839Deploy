#Adam and Bryce's Final Project
import tweepy
from tweepy import OAuthHandler
import regex as re
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

#####Initialization of Class to Do Twitter Client Stuff
class TwitterClient(object):
    '''
    Generic Twitter Class for sentiment analysis.
    '''
    def __init__(self):
        '''
        Class constructor or initialization method.
        '''
        # keys and tokens from the Twitter Dev Console
        consumer_key = "yJsuGs8DcLZjVe4w46RlmE7EU"
        consumer_secret = "7LTHqVUngpY2TnrO2TUKIGDOU3pokGh1s48AhqGDArqrv6ajtv"
        access_token = "1090450437222948864-upQR0M9V0ChS6QKRsRMgsZnBtkZ5oT"
        access_token_secret = "5ntu65BcOUlU1Qwm8Nu369ijMqTkaNhl4CLb60whqXxYQ"

        # attempt authentication
        try:
            # create OAuthHandler object
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            # set access token and secret
            self.auth.set_access_token(access_token, access_token_secret)
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")

    def clean_tweet(self, tweet):
        '''
        Utility function to clean tweet text by removing links, special characters
        using simple regex statements.
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])\
                                    |(\w+:\/\/\S+)", " ", tweet).split())

    def get_tweet_sentiment(self, tweet):
        '''
        Utility function to classify sentiment of passed tweet
        using textblob's sentiment method
        '''
        # create TextBlob object of passed tweet text
        analysis = TextBlob(self.clean_tweet(tweet))
        # set sentiment
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

    def get_tweets(self, query, count = 10):
        '''
        Main function to fetch tweets and parse them.
        '''
        # empty list to store parsed tweets
        tweets = []

        try:
            # call twitter api to fetch tweets
            fetched_tweets = self.api.search(q = query, count = count)

            # parsing tweets one by one
            for tweet in fetched_tweets:
                # empty dictionary to store required params of a tweet
                parsed_tweet = {}
                # saving text of tweet
                parsed_tweet['text'] = tweet.text
                #print(tweet.place)
                # saving sentiment of tweet
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)
                parsed_tweet['date'] = tweet.created_at
                # appending parsed tweet to tweets list
                if tweet.retweet_count > 0:
                    # if tweet has retweets, ensure that it is appended only once
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)
            return tweets

        except tweepy.TweepError as e:
            print("Error : " + str(e))

api = TwitterClient()

with open ('outputBTC.txt', 'rb') as fp1:
	BTC_collected_data = pickle.load(fp1)

with open ('outputTSLA.txt', 'rb') as fp2:
	TSLA_collected_data = pickle.load(fp2)

with open ('outputSPY.txt', 'rb') as fp3:
	SPY_collected_data = pickle.load(fp3)

with open ('outputAAPL.txt', 'rb') as fp4:
	AAPL_collected_data = pickle.load(fp4)

columns_name = ["Price", "Positivity Rate", "Negativity Rate", "Date"]
BTC_df = pd.DataFrame(BTC_collected_data, columns=columns_name)
TSLA_df = pd.DataFrame(TSLA_collected_data, columns=columns_name)
SPY_df = pd.DataFrame(SPY_collected_data, columns=columns_name)
AAPL_df = pd.DataFrame(AAPL_collected_data, columns=columns_name)

BTC_df['Net Sentiment'] = BTC_df['Positivity Rate'] - BTC_df['Negativity Rate']
TSLA_df['Net Sentiment'] = TSLA_df['Positivity Rate'] - TSLA_df['Negativity Rate']
SPY_df['Net Sentiment'] = SPY_df['Positivity Rate'] - SPY_df['Negativity Rate']
AAPL_df['Net Sentiment'] = AAPL_df['Positivity Rate'] - AAPL_df['Negativity Rate']

BTC_df['Correlation'] = BTC_df['Price'].rolling(10).corr(BTC_df['Net Sentiment'])
TSLA_df['Correlation'] = TSLA_df['Price'].rolling(10).corr(TSLA_df['Net Sentiment'])
SPY_df['Correlation'] = SPY_df['Price'].rolling(10).corr(SPY_df['Net Sentiment'])
AAPL_df['Correlation'] = AAPL_df['Price'].rolling(10).corr(AAPL_df['Net Sentiment'])

BTC_df['Stock'] = 'BTC'
TSLA_df['Stock'] = 'TSLA'
SPY_df['Stock'] = 'SPY'
AAPL_df['Stock'] = 'AAPL'

BTC_df['Percent Change'] = BTC_df['Price'].pct_change()
TSLA_df['Percent Change'] = TSLA_df['Price'].pct_change()
SPY_df['Percent Change'] = SPY_df['Price'].pct_change()
AAPL_df['Percent Change'] = AAPL_df['Price'].pct_change()

BTC_df['Sentiment Percent Change'] = BTC_df['Net Sentiment'].pct_change()
TSLA_df['Sentiment Percent Change'] = TSLA_df['Net Sentiment'].pct_change()
SPY_df['Sentiment Percent Change'] = SPY_df['Net Sentiment'].pct_change()
AAPL_df['Sentiment Percent Change'] = AAPL_df['Net Sentiment'].pct_change()


BTC_df.loc[BTC_df['Percent Change']*BTC_df['Sentiment Percent Change'] >= 0, 'Sign of Change'] = "AGREEMENT"
BTC_df.loc[BTC_df['Percent Change']*BTC_df['Sentiment Percent Change'] < 0, 'Sign of Change'] = "NO AGREEMENT"
TSLA_df.loc[TSLA_df['Percent Change']*TSLA_df['Sentiment Percent Change'] >= 0, 'Sign of Change'] = "AGREEMENT"
TSLA_df.loc[TSLA_df['Percent Change']*TSLA_df['Sentiment Percent Change'] < 0, 'Sign of Change'] = "NO AGREEMENT"
SPY_df.loc[SPY_df['Percent Change']*SPY_df['Sentiment Percent Change'] >= 0, 'Sign of Change'] = "AGREEMENT"
SPY_df.loc[SPY_df['Percent Change']*SPY_df['Sentiment Percent Change'] < 0, 'Sign of Change'] = "NO AGREEMENT"
AAPL_df.loc[AAPL_df['Percent Change']*AAPL_df['Sentiment Percent Change'] >= 0, 'Sign of Change'] = "AGREEMENT"
AAPL_df.loc[AAPL_df['Percent Change']*AAPL_df['Sentiment Percent Change'] < 0, 'Sign of Change'] = "NO AGREEMENT"


BTC_df['Percent Change Rolling'] = BTC_df['Percent Change'].rolling(30, win_type='gaussian').sum(std=3)
TSLA_df['Percent Change Rolling'] = TSLA_df['Percent Change'].rolling(30, win_type='gaussian').sum(std=3)
SPY_df['Percent Change Rolling'] = SPY_df['Percent Change'].rolling(30, win_type='gaussian').sum(std=3)
AAPL_df['Percent Change Rolling'] = AAPL_df['Percent Change'].rolling(30, win_type='gaussian').sum(std=3)

BTC_df['Sentiment Percent Change Rolling'] = BTC_df['Sentiment Percent Change'].rolling(10, win_type='gaussian').sum(std=3)
TSLA_df['Sentiment Percent Change Rolling'] = TSLA_df['Sentiment Percent Change'].rolling(10, win_type='gaussian').sum(std=3)
SPY_df['Sentiment Percent Change Rolling'] = SPY_df['Sentiment Percent Change'].rolling(10, win_type='gaussian').sum(std=3)
AAPL_df['Sentiment Percent Change Rolling'] = AAPL_df['Sentiment Percent Change'].rolling(10, win_type='gaussian').sum(std=3)

BTC_df.loc[BTC_df['Sentiment Percent Change Rolling'] >= 0, 'Sign of Sentiment Change'] = "INCREASING SENTIMENT"
BTC_df.loc[BTC_df['Sentiment Percent Change Rolling'] < 0, 'Sign of Sentiment Change'] = "DECREASING SENTIMENT"
TSLA_df.loc[TSLA_df['Sentiment Percent Change Rolling'] >= 0, 'Sign of Sentiment Change'] = "INCREASING SENTIMENT"
TSLA_df.loc[TSLA_df['Sentiment Percent Change Rolling'] < 0, 'Sign of Sentiment Change'] = "DECREASING SENTIMENT"
SPY_df.loc[SPY_df['Sentiment Percent Change Rolling'] >= 0, 'Sign of Sentiment Change'] = "INCREASING SENTIMENT"
SPY_df.loc[SPY_df['Sentiment Percent Change Rolling'] < 0, 'Sign of Sentiment Change'] = "DECREASING SENTIMENT"
AAPL_df.loc[AAPL_df['Sentiment Percent Change Rolling'] >= 0, 'Sign of Sentiment Change'] = "INCREASING SENTIMENT"
AAPL_df.loc[AAPL_df['Sentiment Percent Change Rolling'] < 0, 'Sign of Sentiment Change'] = "DECREASING SENTIMENT"

SPY_df = SPY_df[SPY_df['Sign of Sentiment Change'].notna()]

SPY_df = SPY_df[SPY_df['Sign of Change'].notna()]


ALL_df = pd.concat([BTC_df,TSLA_df,SPY_df])

# print(BTC_df.head())

#### Begin Code for StreamLit App.
st.title("Gaining Insight Through Open Source Information")
st.write("By Adam and Bryce")
st.text("")
st.image("https://pbs.twimg.com/media/C87nB9_XUAAPztm?format=jpg&name=large"\
        ,width=700,layout="centered")
st.text("")
st.title("Introduction")

st.write("In the era of COVID-19, many aspects of day-to-day life are uncertain and subject to rapid change. \
         Meetings and social engagements are cancelled, deadlines are missed, and local government guidelines change daily. \
         Each of these events have major impacts on our daily lives, and rippling impacts on the economy. \
         Beyond these local disturbances, large scale events like positive study results for a vaccine or passage \
         of federal stimulus have major implications for global markets.")

         #Insert graph of unemployment data here

st.write("By carefully tracking major news stories, one can often identify events that will trigger upwards or \
        downwards trends in the market. Since the market is efficient, any newly available information is quickly incorporated into \
        share prices. Once this information is \"built in\" to the price, it is no longer of much value for any person trying to gain \
        an inside track. For this reason, it is important to have a method for identifying relevant information and its impact on the \
        economy. For example, on Monday, March 16th 2020, the S&P 500 fell by nearly 11%. This came on the coattails of President Trump's declaration \
        of a national emergency for Coronavirus after the markets closed the previous Friday [1].")
st.write("In our first series of visualizations, we follow the value of the S&P 500 throughout the pandemic, displaying \
        the SPY exchange traded fund (ETF) first in its traded value over time. Take some time to explore the data in Figure 1 - \
        each data point is clickable, and will redirect you to the New York Times to view the top COVID related articles of that day and the day prior.")

###News Story Graph here
#Altair Plot of SPY, annotated with key news articles...
start_date = '2020-02-01'
end_date = '2020-12-20'
df2 = yf.download("SPY", start = start_date, end = end_date, progress = False)
#print(df2.head(5))

source = pd.DataFrame({
  'Date': df2.index,
  'Price (USD)': df2["Adj Close"]
})

source['DateStr'] = source['Date'].dt.strftime('%Y%m%d')
dateList = source['DateStr'].tolist()
valueList = source['Price (USD)'].tolist()
urlList = []
valueChange = []
prev_date = dateList[0]
for date in dateList:
    urlList.append('https://www.nytimes.com/search?dropmab=true&endDate='+date+'&query=COVID&sort=best&startDate='+prev_date)
    prev_date = date

source['URLs'] = urlList
#Derivative Data for Bar Chart
old_value = valueList[0]
for value in valueList:
    valueChange.append(((value-old_value)/old_value)*100)
    old_value = value

source['Percent_Change'] = valueChange


#print(source.head(5))

chart = alt.Chart(source,title="Figure 1: Value of S&P 500 ETF SPY During COVID19 Pandemic").mark_point().encode(
    x='Date',
    y='Price (USD)',
    tooltip=['Date','Price (USD)'],
    href='URLs'
).interactive().properties(
    width=600,
    height=500)

st.write(chart)

chart2 = alt.Chart(source,title="Figure 2: Day to Day Percent Change of S&P 500").mark_bar().encode(
    x="Date",
    y="Percent_Change",
    color=alt.condition(
        alt.datum.Percent_Change > 0,
        alt.value("black"),  # The positive color
        alt.value("red")  # The negative color
    ),
    tooltip=['Date','Percent_Change'],
    href='URLs'
).properties(width=600).interactive()


st.write("Perhaps a more compelling visualization of this data is to inspect the relative change in the market on a day to day basis. \
        By visualizing the percentage increase or decrease of the market each day, it is easier to identify where one should search for major \
        news events. Below, Figure 2 also allows you to click through and search for news articles associated with a particular day. Looking at Figure 2, the largest single day percent gain during \
        this time period occurred on March 24th. The day prior, The White House Coronavirus Task Force made an announcement arguing against shut downs \
        and encouraging state and local leaders to keep the economy open [2]. This clearly signaled positivity about the future of the economy and thus \
        helped drive the market rally the next day.")

st.write(chart2)

# chart3 = alt.Chart(BTC_df,title="Figure 3: Value of S&P 500 ETF SPY During COVID-19 Pandemic").mark_point().encode(
#     x='Date',
#     y='Price',
#     tooltip=['Date','Price'],
# #     href='URLs'
# 	scale=alt.Scale(zero=False)
# ).interactive().properties(
#     width=600,
#     height=400)

st.write("Beyond market trends as a whole, this kind of news analysis can also prove useful for individual stocks. News articles can often explain \
        why a stock is outpacing the growth of the market or lagging behind. In the \"Try it Yourself!\" section below you can do your own \
        research. One interesting thread is to input TSLA as your stock ticker. You will quickly notice that TSLA had an incredibly \
        large drop (-21.1%) on September 8th, 2020. Clicking through the link for this date will show you that this was the result of Tesla \
        being snubbed by the S&P 500 and kept off of that index [3].")
st.write("")
tryout = st.beta_expander("Try it yourself! Analyze Trading Data.")
with tryout:
    st.write("Input a stock of your own choosing and view personalized versions of Figures 1 and 2, \
    as well as search results for each day.")
    user_choice = st.text_input('Input Ticker:', '')
    #Verify it's a real ticker.
    if(user_choice):
        df3 = yf.download(user_choice, start = start_date, end = end_date, progress = False)
        if(df3.empty):
            st.write("Invalid ticker, please enter a different one.")
        else:
            #Calculate A bunch of Stuff
            source2 = pd.DataFrame({
              'Date': df3.index,
              'Price (USD)': df3["Adj Close"]
            })

            source2['DateStr'] = source2['Date'].dt.strftime('%Y%m%d')
            dateList2 = source2['DateStr'].tolist()
            valueList2 = source2['Price (USD)'].tolist()
            urlList2 = []
            valueChange2 = []
            prev_date2 = dateList2[0]
            for date in dateList2:
                #urlList2.append('https://www.nytimes.com/search?dropmab=true&endDate='+date+'&query=COVID&sort=best&startDate='+prev_date)
                urlList2.append('https://www.marketwatch.com/search?q='+user_choice+'&m=Ticker&rpp=15&mp=2005&bd=true&bd=false&bdv='\
                +date[4:6]+'%2F'+date[6:8]+'%2F'+date[0:4]+'&rs=true')
                prev_date2 = date

            source2['URLs'] = urlList2
            #Derivative Data for Bar Chart
            old_value2 = valueList2[0]
            for value in valueList2:
                valueChange2.append(((value-old_value2)/old_value2)*100)
                old_value2 = value

            source2['Percent_Change'] = valueChange2

            #Make charts
            chart3 = alt.Chart(source2,title="Value of " +user_choice+" During COVID19 Pandemic").mark_point().encode(
                x='Date',
                y='Price (USD)',
                tooltip=['Date','Price (USD)'],
                href='URLs'
            ).interactive().properties(
                width=550,
                height=400)

            st.write(chart3)

            chart4 = alt.Chart(source2,title="Day to Day Percent Change of "+user_choice).mark_bar().encode(
                x="Date",
                y="Percent_Change",
                color=alt.condition(
                    alt.datum.Percent_Change > 0,
                    alt.value("black"),  # The positive color
                    alt.value("red")  # The negative color
                ),
                tooltip=['Date','Percent_Change'],
                href='URLs'
            ).properties(width=550).interactive()

            st.write(chart4)
st.write("")
st.title("Open Source Information")
st.write("Beyond mediums like news articles or broadcasts, there are many different avenues through which information \
         relevant to the market could be found. \"Open source information\" can be defined as any information that is publicly available, \
         and can be obtained by request, purchase, or observation [4]. Although this kind of information is publicly available, it could be difficult \
         or expensive to obtain. For many machine learning applications, open source information is drawn from large companies like Facebook, Google, \
         and Twitter. Although data obtained through these company's APIs has some metadata tagging, it still needs to be further cleaned and analyzed.")
st.write("Just like articles from news media can have an impact on the market on large time scales, it follows that smaller events that are much more immediate \
        and time sensitive could impact the stock market in real time. For example, on May 1st 2020, Elon Musk tweeted \"Tesla stock price is too high imo,\" \
        which sent the company's stock value into a -10% nosedive almost immediately [5]. In this case, only the savviest and quickest investors would have \
        been able to see this tweet and sell prior to the inevitable drop." )
st.image("https://static.toiimg.com/photo/imgsize-11092,msid-75579881/75579881.jpg",caption="The Tweet Heard \'Round the World!")
st.write("Right now it is hard to imagine how one might automatically incorporate this type of information into any model about the stock market. \
        Although humans can easily read and interpret a tweet such as the one from Mr. Musk, writing an algorithm or model to do this is \
        no easy task. In order to apply a machine learning aspect to this problem, we pursued an approach based on analyzing the sentiment of tweets \
        about a chosen keyword.")
st.write("For our sentiment analysis we used TextBlob, which is a natural language processing (NLP) package for Python [6]. TextBlob is able to perform \
        many language processing tasks, including word lemmatization and inflection, noun-phrase extraction, and part of speech tagging. The feature in \
        particular that we care about is sentiment classification. TextBlob is able to classify the polarity of text (positive or negative) as well as \
        the subjectivity of a given text (fact or opinion) [7].")
st.write("")

tryout2 = st.beta_expander("Try it yourself! Sentiment Classification.")
with tryout2:
    st.write("Input a sentence or phrase below to try out sentiment classification for yourself:")
    myPhrase = st.text_input('Input Phrase:', '')
    phrase_blob = TextBlob(myPhrase)
    if(myPhrase):
        if(phrase_blob.sentiment.polarity>0):
            st.write("Classified as positive.")
        if(phrase_blob.sentiment.polarity==0):
            st.write("Classified as neutral.")
        if(phrase_blob.sentiment.polarity<0):
            st.write("Classified as negative.")
st.write("")
st.write("With the sentiment classification aspect sorted, the next step is to gather data from Twitter. We did this by applying for Twitter API access credentials \
        and then using that API in order to make queries for tweets about a specific keyword. Although the Twitter API is quite useful (and free!) there are \
        certain limitations that one has to work around while using it. The first major limitation of the API is that query size is restricted to 100 tweets. \
        This means that any keyword request made through the API can at most contain 100 responses. Because of this limitation and the bursty nature of tweeting, \
        queries can often end up with many duplicate tweets because of many users retweeting a particularly popular post in a short period of time. A second limitation \
        of the API is that the default behavior is to provide the 100 most recent tweets matching a keyword as the query response. There are workarounds to look for specific \
        time periods, however this is still limited to a 7 day window prior to the current time. As a result, it is difficult to use the API approach in order to research things \
        in the past like the market at the beginning of the COVID period. We designed our data collection to work around these limitations by writing a program to gather market \
        data and batches of tweets simultaenously throughout a trading day. Using this script, we collected data for a few search terms, including AAPL, TSLA, BTC, and COVID19.")

tryout3 = st.beta_expander("Try it yourself! Twitter Keyword Search and Classification.")
with tryout3:
    st.write("Input a keyword search to fetch up to three tweets.")
    myPhrase2 = st.text_input('Search Term:', '')
    if(myPhrase2):
        api = TwitterClient()
        tweets = api.get_tweets(query = myPhrase2, count = 3)
        for tweet in tweets:
            st.write("Text: "+tweet['text'])
            st.write("Classification: "+tweet['sentiment'])
            st.markdown("---")
st.markdown("---")
st.write("Following from the idea that particularly consequential tweets could result in major swings \
        in a company’s value, we also wanted to visualize how tweets from a particularly important individual \
        (Elon Musk in this case), could impact share price over a longer period of time. In the chart below, \
        the average sentiment of Musk’s tweets on a daily basis are layered with a plot of TSLA’s share price \
        over the same time period. Each tweet was classified using the TextBlob method described above. After \
        classification, tweets were binned by date to compute an average sentiment for the day. Inspecting this \
        graph closely, you can see that very negatively and very positively polarized tweeting days are often nearby \
        days with large deltas in share price. Although this does not allow us to draw any conclusions about \
        causality or the extent to which these two phenomenon are intertwined, it does give us pause to investigate further. ")

st.image("https://i.ibb.co/RzYDpPQ/Screen-Shot-2020-12-09-at-10-25-06-PM.png",width=700)

st.title("Sentiment Analysis - Day Scale")

st.write("In this section, we examine visualizations for Bitcoin, Tesla, and the SPDR S&P 500 ETF. \
		These data were collected over a single trading day using a Tweet Miner, as described above. \
		Three encodings are used to represent the data: color for strength of the correlation \
		between the price of the asset and the Twitter sentiment; size to denote the net sentiment \
		calculated as the difference between the rate of positive tweets and negative tweets about the asset; \
		and shape to denote if the sign of the derivatives of the price and sentiment data are in agreement \
		or not.")

chart_b_1 = alt.Chart(BTC_df).mark_point().encode(
    alt.X('Date',
        scale=alt.Scale(zero=False)
    ),
    y = alt.Y('Price', scale=alt.Scale(zero=False)),
    color = 'Correlation',
    fill = 'Correlation',
    size = 'Net Sentiment',
    shape = 'Sign of Change',
    tooltip=['Date','Price','Net Sentiment','Correlation']
).properties(width=700, height = 400, title = 'Sentiment and Correlation of BTC').interactive()

st.write(chart_b_1)

st.write("Beginning at 4:20, we begin to see relatively strong correlation between tweet sentiment \
		and asset price. At 4:20, 4:25, and 4:30, tweet sentiment seems to act as a support for \
		the price. Furthermore, in the 4:30 step, we see agreement between the signs of the derivative of \
		the asset price and the derivative of the tweet sentiment, suggesting that these two metrics are \
		moving in the same direction. However, at 4:35, we see these signs diverge and the support falls apart, \
		which leads to the stock price falling.")

chart_b_2 = alt.Chart(TSLA_df).mark_point().encode(
    alt.X('Date',
        scale=alt.Scale(zero=False)
    ),
    y = alt.Y('Price', scale=alt.Scale(zero=False)),
    color = 'Correlation',
    fill = 'Correlation',
    size = 'Net Sentiment',
    shape = 'Sign of Change',
    tooltip=['Date','Price','Net Sentiment','Correlation']
).properties(width=700, height = 400, title = 'Sentiment and Correlation of TSLA').interactive()

st.write(chart_b_2)

st.write("Beginning at 12:05, we see a reversal in the stock price as the price begins to rise. \
	When the reversal occurs, the net sentiment is approximately 25% and the correlation is -40%. \
	However, there is agreement between the derivatives of the stock price and the Twitter sentiment. \
	As the stock price rises, the net sentiment strenghtens to 33%, and the correlation increases to 86%. \
	When the stock price finally goes down at 12:10, the event is marked by divergence between the \
	derivatives of the stock price and the Twitter sentiment, even while the sentiment and correlation \
	remain high. This suggests that examining the agreement of the derivatives is the key indicator for \
	the reversal at 12:10.")

chart_b_3 = alt.Chart(SPY_df).mark_point().encode(
    alt.X('Date',
        scale=alt.Scale(zero=False)
    ),
    y = alt.Y('Price', scale=alt.Scale(zero=False)),
    color = 'Correlation',
    fill = 'Correlation',
    size = 'Net Sentiment',
    shape = 'Sign of Change',
    tooltip=['Date','Price','Net Sentiment','Correlation']
).properties(width=700, height = 400, title = 'Sentiment and Correlation of SPY').interactive()

st.write(chart_b_3)

st.write("Investigating this plot, there are a few interesting trends to look at. One thing in particular that this visualization brings to the forefront, \
        is that the correlation between our collected tweet sentiment data and the  pricing of the index grows largest during the periods of high \
        volatility. This is denoted by the darker shading of the data points in the graph when it is at its steepest sections. \
        Zooming in to the chart to inspect closely, it appears that the correlation of of the sentiment analysis and stock \
        pricing becomes most uncertain immediately prior to local maxima and minima. If one were to trade of this information, \
        this could mean that low or negative correlation between tweets and index pricing is a signal that a maxima or minima would occur. \
        If, for example one had sold 1000 shares of SPY at roughly 3:38 PM when the correlation transitioned from positive to negative, \
        the sale would have fetched $36,874. Using that money to repurchase shares of SPY when the correlation turned around at 3:45 PM would \
        net the purchaser a 0.2 more shares than they had before. Repeated over larger time scales, this approach could result in nontrivial gains. \
        Noise trading approaches leverage sophisticated algorithms to exploit small trends like this for similar arbitrage opportunities. ")

# chart_b_4 = alt.Chart(ALL_df).mark_point().encode(
#     alt.X('Date',
#         scale=alt.Scale(zero=False)
#     ),
#     y = alt.Y('Percent Change', scale=alt.Scale(zero=False)),
#     color = 'Stock',
#     fill = 'Stock',
#     size = 'Correlation',
#     tooltip=['Date','Price','Net Sentiment','Correlation']
# ).properties(width=700, height = 400, title = 'Sentiment and Correlation of BTC, TSLA, and SPY').interactive()
#
# st.write(chart_b_4)

st.write("In the final demonstration, we visualize information about the derivative of the asset price \
		and the derivative of tweet sentiment. Furthermore, in order to reduce the noise of these metrics, \
		we have computed 30-minute rolling averages of the derivative data. The data are encoded as follows: \
		size is used to denote the strength of the correlation between the change in asset price and the change \
		in tweet sentiment. The shape is used to denote whether tweet sentiment is increasing or decreasing. \
		Lastly, color is used to denote the three different assets: Bitcoin, the SPDR S&P 500 ETF, and Tesla. NOTE: \
		the asset symbols can be selected in order to highlight the data for a particular asset.")

selection = alt.selection_multi(fields=['Stock'])
color = alt.condition(selection,
                      alt.Color('Stock:N', legend=None),
                      alt.value('lightgray'))


chart_b_5 = alt.Chart(ALL_df).mark_point().encode(
    x = alt.X('Date', scale=alt.Scale(zero=False)),
    y = alt.Y('Percent Change Rolling:Q', scale=alt.Scale(zero=False)),
    color=color,
    shape = 'Sign of Sentiment Change',
    size = 'Correlation',
    tooltip=['Date','Price','Net Sentiment','Correlation']
).properties(width=700, height = 400, title = 'Sentiment and Correlation of BTC, TSLA, and SPY').interactive()

legend = alt.Chart(ALL_df).mark_point().encode(
    y=alt.Y('Stock:N', axis=alt.Axis(orient='right')),
    color=color
).add_selection(
    selection
)

chart_b_5 | legend

st.write("Intuitively, we would expect that increasing tweet sentiment would accompany an increasing stock asset, \
		and decreasing tweet sentiment would accompany a decreasing asset price.")

st.write("Sometimes, we observe this intuition being satisfied. For example, between 2:45 and 3:00, the price of Tesla is \
		increasing while the Twitter sentiment is also increasing. Likewise, from 12:10 to 12:20, the price of Bitcoin \
		decreases as the Twittter sentiment also decreases.")

st.write("However, it is also possible to observe many instances in which the intuitive relationship between asset price \
		and twitter sentiment is not positively correlated. For example, it is often the case that \
		the stock price decreases as tweet sentiment is increasing, while the converse is also often true. For \
		example, between 1:15 and 1:35, the price of Bitcoin is going down while net Bitcoin tweet sentiment is \
		going up. Furthermore, between 1:00 and 1:20, the price of Tesla is increasing with the Twitter sentiment is \
		decreasing. This leads us to conclude that there is not a reliable pattern between asset price and tweet sentiment. ")

# input_dropdown = alt.binding_select(options=['BTC','SPY','TSLA'])
# selection = alt.selection_single(fields=['Stock'], bind=input_dropdown, name='Country of ')
# color = alt.condition(selection,
#                     alt.Color('Origin:N', legend=None),
#                     alt.value('lightgray'))
#
# alt.Chart(ALL_df).mark_point().encode(
#     alt.X('Date',
#         scale=alt.Scale(zero=False)
#     ),
#     y = alt.Y('Percent Change', scale=alt.Scale(zero=False)),
#     color = 'Stock',
#     fill = 'Stock',
#     size = 'Correlation',
#     tooltip=['Date','Price','Net Sentiment','Correlation']
# ).add_selection(
#     selection
# )

# chart_b_4 = alt.Chart(AAPL_df).mark_point().encode(
#     alt.X('Date',
#         scale=alt.Scale(zero=False)
#     ),
#     y = alt.Y('Price', scale=alt.Scale(zero=False)),
#     color = 'Correlation',
#     fill = 'Correlation',
#     size = 'Net Sentiment',
#     tooltip=['Date','Price','Net Sentiment','Correlation']
# ).properties(width=700).interactive()
#
# st.write(chart_b_4)

st.title("References")
st.write("[1] https://www.nytimes.com/video/us/politics/100000007032704/trump-coronavirus-live.html?searchResultPosition=2")
st.write("[2] https://www.nytimes.com/video/us/politics/100000007049048/white-house-coronavirus-press-conference-live.html?searchResultPosition=7")
st.write("[3] https://www.marketwatch.com/story/sp-500-adds-three-companies-not-named-tesla-sending-car-companys-shares-down-2020-09-04")
st.write("[4] http://press-files.anu.edu.au/downloads/press/p125391/html/ch03s03.html")
st.write("[5] https://www.dw.com/en/tesla-shares-tumble-as-musk-says-companys-stock-is-overvalued/a-53308317")
st.write("[6] https://www.geeksforgeeks.org/twitter-sentiment-analysis-using-python/")
st.write("[7] https://www.analyticsvidhya.com/blog/2018/02/natural-language-processing-for-beginners-using-textblob/")
# st.title("Sentiment Analysis")
# st.write("Let's look at sentiment information for a few different topics. First, we will look at the election.")
# st.write("Using the Twitter API, we pulled the most recent million tweets about the U.S. Election. After running these tweets through a sentiment classifier, \
#          we generated wordclouds that reflect the twenty most commonly used words or phrases within each classification (positive or negative).")
# st.image(image_1, caption='Top 20 Words in Negative Tweets about Election',use_column_width= True)
# st.image(image_2, caption='Top 20 Words in Positive Tweets about Election',use_column_width= True)
# st.write("These Wordclouds are great summary visualizations because they can quickly give us information. For example, the tweets classified as \
#         negative tend to have a greater occurrence of the word Trump vs. the word Biden. Additionally, words like Fraud, or Hoax appear in negative tweets, \
#         whereas words like Audit, or Certify appear in positive ones.")
