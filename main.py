import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
from tween import count_tweets

if __name__ == '__main__':
    with st.spinner('Wait for it...'):
        #st.title('Twitter analyzer')
        search_for = st.text_input('Subject')

        if len(search_for)>0:
            data = count_tweets(search_for)
            fig = px.scatter(data, x="Date", y="Number of tweets",
                       title="Number of tweets during last hour")
            fig.update_layout(title_yanchor='middle')
            st.plotly_chart(fig)
