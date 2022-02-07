import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
from tween import *

if __name__ == '__main__':
    with st.spinner('Wait for it...'):
        st.title('Metrics by subject')
        search_for = st.text_input('Subject')

        st.header('Part 1')
        granularity = st.radio("Granularity of the tweets",
                               ('Day', 'Hour', 'Minute'),
                               key='Day')
        if len(search_for)>0:
            # count number of tweets
            data = count_tweets(search_for, granularity)
            fig = px.scatter(data, x="Date", y="Number of tweets",
                       title=f"Number of tweets during last {granularity.lower()}s")
            fig.update_layout(title_yanchor='bottom')
            st.plotly_chart(fig)

            # add tweets data
            st.header('Advanced Metrics')
            df = format_tweet_data(tweets_by_subject(subject=search_for, nb_max=4))
            st.text(f'The following metrics are based on the most recent tweets during '
                    f'the last 7 days')
            st.text(f'Number of tweets {df.shape[0]}')
            col1, col2 = st.columns(2)
            col1.metric("Min Date", str(df.created_at.min())[:19])
            col2.metric("Max Date", str(df.created_at.max())[:19])
            #col3.metric("Number of Tweets", df.shape[0])

            # This dataframe has 244 lines, but 4 distinct values for `day`
            type_tweets = round(df.referenced_tweets.value_counts(normalize=True), 2)
            fig2 = px.pie(values=type_tweets, names=[(x.replace('_', ' ')).capitalize() for x in type_tweets.index])
            st.plotly_chart(fig2)
