import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
from tween import *

if __name__ == '__main__':
    st.set_page_config(layout="wide")

    with st.spinner('Wait for it...'):
        st.title('Metrics by subject')
        search_for = st.text_input('Subject')

        st.header('Part 1')
        # c1, c2 = st.columns(2)
        granularity = st.radio("Granularity of the tweets",
                               ('Day', 'Hour', 'Minute'),
                               key='Day')

        if len(search_for) > 0:
            # count number of tweets
            data = count_tweets(search_for, granularity)
            fig = px.scatter(data, x="Date", y="Number of tweets",
                             title=f"Number of tweets during last {granularity.lower()}s")
            fig.update_layout(title_yanchor='bottom')
            st.plotly_chart(fig, use_container_width=True)

            # add tweets data
            st.header('Advanced Metrics')
            twts = st.slider('How much tweets do you want to load ? (hundreds)', 0, 15, 2)

            df = format_tweet_data(tweets_by_subject(subject=search_for, nb_max=twts))
            st.markdown(f'The following metrics are based on the most recent tweets during '
                        f'the last 7 days')
            col1, col2, col3 = st.columns(3)
            col1.metric("Min Date", str(df.created_at.min())[:19])
            col2.metric("Max Date", str(df.created_at.max())[:19])
            col3.metric("Number of tweets", str(df.shape[0]))

            user_count = (df[['username', 'referenced_tweets']].value_counts())
            col1.metric("Number of different users", str(len(user_count)))
            col2.metric("Mean tweets per user", str(user_count.mean())[:4])
            col3.metric("Median tweets per user", str(user_count.median())[:4])
            fig4 = px.bar(x=user_count.index.get_level_values(0)[:10], y=user_count[:10],
                          color=user_count.index.get_level_values(1)[:10],
                          labels={'x': 'Username',
                                  'y': 'Number of tweets'})
            st.plotly_chart(fig4, use_container_width=True)

            # This dataframe has 244 lines, but 4 distinct values for `day`
            type_tweets = round(df.referenced_tweets.value_counts(normalize=True), 2)
            device = round(df.source.value_counts(normalize=True), 2)

            fig2 = px.pie(values=type_tweets, names=[(x.replace('_', ' ')).capitalize() for x in type_tweets.index],
                          title='Type of tweet repartition')
            fig3 = px.pie(values=device, names=[(x.replace('_', ' ')).capitalize() for x in device.index],
                          title='Device repartition')
            c1b, c2b = st.columns(2)
            c1b.plotly_chart(fig2, use_container_width=True)
            c2b.plotly_chart(fig3, use_container_width=True)
