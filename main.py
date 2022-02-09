import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
from tween import *
import plotly.graph_objects as go


def dataframe_px(data: pd.DataFrame):
    fig = go.Figure(data=[go.Table(
        columnorder=[1, 2, 3],
        columnwidth=[200, 300, 900],
        header=dict(
            values=[['Username'], ['Type'],
                    ['Content']],
            line_color='darkslategray',
            fill_color='royalblue',
            align=['left', 'center'],
            font=dict(color='white', size=12),
            height=40
        ),
        cells=dict(
            values=[data.username.tolist(), data.referenced_tweets.tolist(), data.text.tolist()],
            line_color='darkslategray',
            fill=dict(color=['paleturquoise', 'white']),
            align=['left', 'center'],
            font_size=12,
            height=30)
    )
    ])
    return fig


if __name__ == '__main__':
    st.set_page_config(layout="wide")

    st.title('Explore trends')

    country_list = ['None'] + [k for k, v in woeid.items()]
    trend = 'None'

    country = st.selectbox('Select trends country :',
                           country_list
                           )

    if country != 'None':
        trends_list = ['None'] + get_trends(country)
        trend = st.selectbox('Select trend if you want :',
                             trends_list,
                             index=0
                             )

    with st.expander('Other options (end date...)'):
        st.markdown('Soon...or not')

    with st.spinner('Wait for it...'):
        st.title('Metrics by subject')

        if isinstance(trend, str) & (trend != 'None'):
            trend = ''.join((trend.split(' ')[1:]))

        search_for = st.text_input('Subject',
                                   value=trend
                                   )

        st.header('Part 1')
        # c1, c2 = st.columns(2)
        granularity = st.radio("Granularity of the tweets",
                               ('Day', 'Hour', 'Minute'),
                               key='Day'
                               )

        if len(search_for) > 0:
            # count number of tweets
            data = count_tweets(search_for,
                                granularity
                                )
            fig = px.area(data, x="Date",
                          y="Number of tweets",
                          title=f"Number of tweets during last {granularity.lower()}s"
                          )
            fig.update_layout(title_yanchor='bottom')
            st.plotly_chart(fig,
                            use_container_width=True
                            )

            # add tweets data
            st.header('Advanced Metrics')

            tweet_type = st.multiselect(
                'Tweet type filter :',
                ['tweet', 'retweeted', 'quoted', 'replied_to'],
                ['tweet', 'retweeted', 'quoted', 'replied_to']
            )

            twts = st.slider('How much tweets do you want to load ? (hundreds)',
                             2,
                             20,
                             2
                             )

            df_ = format_tweet_data(*tweets_by_subject(subject=search_for,
                                                       nb_max=int(twts)),)
            df = df_[df_.referenced_tweets.isin(tweet_type)].reset_index(drop=True)

            st.markdown(f'The following metrics are based on the most recent tweets during '
                        f'the last 7 days')

            # Useful metrics
            col1, col2, col3 = st.columns(3)
            col1.metric("Min Date",
                        str(df.tweet_date.min())[:19]
                        )
            col2.metric("Max Date",
                        str(df.tweet_date.max())[:19]
                        )
            col3.metric("Number of tweets",
                        str(df.shape[0])
                        )

            user_count = df[['username', 'referenced_tweets']].value_counts()

            col1.metric("Number of different users",
                        str(len(user_count)))

            col2.metric("Ratio tweets/unqiue user",
                        str(round(df.shape[0] / len(user_count),
                                  2))
                        )

            col3.metric("First tweet by",
                        str(df['username'][df.tweet_date.idxmax()])
                        )


            fig4 = px.bar(x=user_count.index.get_level_values(0)[:10],
                          y=user_count[:10],
                          color=user_count.index.get_level_values(1)[:10],
                          labels={'x': 'Username',
                                  'y': 'Number of tweets'}
                          )
            st.plotly_chart(fig4,
                            use_container_width=True
                            )

            with st.expander('Tweets content'):
                st.plotly_chart(dataframe_px(df[['username', 'referenced_tweets', 'text']][
                    df.username.isin(user_count.index.get_level_values(0)[:10])].reset_index(
                    drop=True)),
                    use_container_width=True
                )
                st.dataframe(df)

            # This dataframe has 244 lines, but 4 distinct values for `day`
            type_tweets = round(df.referenced_tweets.value_counts(normalize=True),
                                2
                                )
            device = round(df.source.value_counts(normalize=True),
                           2
                           )

            fig2 = px.pie(values=type_tweets, names=[(x.replace('_', ' ')).capitalize() for x in type_tweets.index],
                          title='Type of tweet repartition')
            fig3 = px.pie(values=device, names=[(x.replace('_', ' ')).capitalize() for x in device.index],
                          title='Device repartition')
            c1b, c2b = st.columns(2)
            c1b.plotly_chart(fig2, use_container_width=True)
            c2b.plotly_chart(fig3, use_container_width=True)
