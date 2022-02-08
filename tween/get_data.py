import requests
from tween.credentials import TOKEN
import json
import pandas as pd
import plotly.express as px
import streamlit as st

woeid = {'France': '23424819', 'USA': '23424977',
         'UK': '23424975','Spain': '23424950',
         'Belgium': '23424757', 'Canada': '23424775'}

@st.cache
def count_tweets(subject: str, granularity: str = 'hour'):
    subject = subject.replace(' ', '%20')
    subject = subject.replace('#', '%23')

    url = f"https://api.twitter.com/2/tweets/counts/recent?query={subject}&granularity={granularity.lower()}"

    payload = {}
    headers = {
        'Authorization': f'Bearer {TOKEN}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    data = json.loads(response.text)['data']
    data = pd.json_normalize(data)
    data['end'] = pd.to_datetime(data.end)
    data = data.rename(columns={'end': 'Date',
                                'tweet_count': 'Number of tweets'})
    # print(data)

    return data

@st.cache(show_spinner=False)
def tweets_by_subject(subject: str, meta_token: str = '', granularity: str = 'hour', cnt: int = 1, nb_max=2):
    subject = subject.replace(' ', '%20')
    subject = subject.replace('#', '%23')

    if (cnt > int(nb_max)):
        return []

    if len(meta_token) != 0:
        url = f"https://api.twitter.com/2/tweets/search/recent?max_results=100&next_token={meta_token}&tweet.fields=author_id,created_at,entities,in_reply_to_user_id,source,attachments,conversation_id,public_metrics,referenced_tweets&query={subject}"
    else:
        url = f"https://api.twitter.com/2/tweets/search/recent?max_results=100&tweet.fields=author_id,created_at,entities,in_reply_to_user_id,source,attachments,conversation_id,public_metrics,referenced_tweets&query={subject}"

    payload = {}
    headers = {
        'Authorization': f'Bearer {TOKEN}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    if (response.status_code != 200):
        return []

    data = json.loads(response.text)['data']
    meta = json.loads(response.text)['meta']

    if ('next_token' in (c := meta)):
        cnt += 1
        new = tweets_by_subject(subject=subject,
                                meta_token=c['next_token'],
                                granularity=granularity,
                                cnt=cnt, nb_max=nb_max)
        if len(new) > 0:
            data = data + new

    return data

@st.cache(show_spinner=False)
def format_tweet_data(data) -> pd.DataFrame:
    df = pd.json_normalize(data)
    df = df[['author_id', 'referenced_tweets', 'conversation_id', 'source', 'text',
             'created_at', 'id', 'public_metrics.retweet_count',
             'public_metrics.reply_count', 'public_metrics.like_count',
             'public_metrics.quote_count', 'entities.mentions']]
    df['referenced_tweets'] = df['referenced_tweets'].apply(lambda x: x[0]['type'] if type(x) is list else 'tweet')
    df['entities.mentions'] = df['entities.mentions'].apply(
        lambda x: x[0]['username'] if type(x) is list else 'User not found')
    df.rename(columns={'entities.mentions': 'username'}, inplace=True)
    df.created_at = pd.to_datetime(df.created_at)
    df = df.drop_duplicates(subset=['created_at', 'author_id', 'text', 'id'])
    # print(df)
    return (df.reset_index())



@st.cache(show_spinner=False)
def get_trends(country: str):

    url = f"https://api.twitter.com/1.1/trends/place.json?id={woeid[country]}"

    payload = {}
    headers = {
        'Authorization': f'Bearer {TOKEN}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    if (response.status_code != 200):
        return []

    data = json.loads(response.text)[0]['trends']
    trends = [(str(k+1)+ ') '+str(j['name'])) for k, j in enumerate(data)]
    #[k if (k is not None) else (0) for k in data['tweet_volume']]
    return trends

# def get_count_reference_by_user(data: pd.DataFrame) -> pd.DataFrame:

# format_tweet_data(tweets_by_subject('senegal'))
# count_tweets('ASMOL')
