#Adam and Bryce's Final Project! Woohoo!
import tweepy
from PIL import Image

# consumer_key = "wXXXXXXXXXXXXXXXXXXXXXXX1"
# consumer_secret = "qXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXh"
# access_token = "9XXXXXXXX-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXi"
# access_token_secret = "kXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXT"

import streamlit as st
image_1 = Image.open('Election_neg.png')
image_2 = Image.open('Election_pos2.png')

st.title("Mining Twitter Data for Fun and Profit")
st.write("By Bryce and Adam")
st.text("")
st.text("")
st.title("Introduction")
st.write("Through the democratization of technology and information, it is possible now more than ever for \
        invididuals to conduct research of large datasets and arrive at novel and interesting conclusions.\
        By leveraging open source information such as published datasets or APIs, it is possible for data \
        scientists to aggregate and parse enough information to make predictions about the performance and outcomes \
        of things like product launches, share prices, or political events. However, it is not immediately clear \
        which research avenues are likely to have the greatest accuracy.")
st.write("In this project we seek to answer this research question by mining twitter data to analyze the trends \
        and sentiment surrounding a few curated topics. For each of these topics our ultimate goal is to assess \
        the correlation between our analysis of tweets, and the outcomes of the topic in reality.")
st.write("An interesting aspect of the Twitter API that we had to work around was the fact that it limits searches to a \
        time depth of one week. This means that our research had to consider only events that were timely to our research. \
        Fortunately, as you will be able to see in our first cut analysis, Apple had a significant product launch of their M1 \
        series chips during our research. Another interesting aspect of this research is that sentiment analysis seems to work \
        best against less nuanced topics. For instance, the sentiment classifier tends to work well with tweets about products \
        (such as reviews, where headlines are intended to clearly transmit sentiment), but not as well with news stories. Unlike reviews, \
        news stories are not as easily classified as positive or negative, and certainly have more complexity in their construction.")

st.title("Sentiment Analysis")
st.write("Let's look at sentiment information for a few different topics. First, we will look at the election.")
st.write("Using the Twitter API, we pulled the most recent million tweets about the U.S. Election. After running these tweets through a sentiment classifier, \
         we generated wordclouds that reflect the twenty most commonly used words or phrases within each classification (positive or negative).")
st.image(image_1, caption='Top 20 Words in Negative Tweets about Election',use_column_width= True)
st.image(image_2, caption='Top 20 Words in Positive Tweets about Election',use_column_width= True)
st.write("These Wordclouds are great summary visualizations because they can quickly give us information. For example, the tweets classified as \
        negative tend to have a greater occurrence of the word Trump vs. the word Biden. Additionally, words like Fraud, or Hoax appear in negative tweets, \
        whereas words like Audit, or Certify appear in positive ones.")
