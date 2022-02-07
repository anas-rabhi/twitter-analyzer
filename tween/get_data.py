import requests
from tween.credentials import TOKEN
import json
import pandas as pd
import plotly.express as px

def count_tweets(subject: str, granularity: str = 'hour'):
  subject = subject.replace(' ', '%20')
  subject = subject.replace('#', '%23')

  url = f"https://api.twitter.com/2/tweets/counts/recent?query={subject}&granularity={granularity.lower()}"

  payload={}
  headers = {
    'Authorization': f'Bearer {TOKEN}'
  }

  response = requests.request("GET", url, headers=headers, data=payload)
  data = json.loads(response.text)['data']
  data = pd.json_normalize(data)
  data['end'] = pd.to_datetime(data.end)
  data = data.rename(columns={'end': 'Date',
                              'tweet_count': 'Number of tweets'})
  #print(data)

  return data

def tweets_by_subject(subject: str, meta_token: str = '', granularity: str = 'hour', cnt: int = 1, nb_max = 2):
  subject = subject.replace(' ', '%20')
  subject = subject.replace('#', '%23')

  if (cnt>int(nb_max)):
    return []

  if len(meta_token)!=0:
    url = f"https://api.twitter.com/2/tweets/search/recent?max_results=100&next_token={meta_token}&tweet.fields=author_id,created_at,in_reply_to_user_id,source,attachments,conversation_id,public_metrics,referenced_tweets&query={subject}"
  else:
    url = f"https://api.twitter.com/2/tweets/search/recent?max_results=100&tweet.fields=author_id,created_at,in_reply_to_user_id,source,attachments,conversation_id,public_metrics,referenced_tweets&query={subject}"

  payload = {}
  headers = {
    'Authorization': f'Bearer {TOKEN}'
  }

  response = requests.request("GET", url, headers=headers, data=payload)
  if (response.status_code!=200):
    return []


  data = json.loads(response.text)['data']
  meta = json.loads(response.text)['meta']

  if ('next_token' in (c := meta)):
    cnt += 1
    new = tweets_by_subject(subject=subject,
                                         meta_token=c['next_token'],
                                         granularity=granularity,
                                         cnt=cnt, nb_max=nb_max)
    if len(new)>0:
      data = data + new

  return data

def format_tweet_data(data):
  df = pd.json_normalize(data)
  df.referenced_tweets = df.referenced_tweets.apply(lambda x: x[0]['type'] if type(x) is list else 'tweet')
  df.created_at = pd.to_datetime(df.created_at)
  df = df.drop_duplicates(subset=['created_at', 'author_id', 'text', 'id'])
  #print(df)
  return (df.reset_index())


#format_tweet_data(tweets_by_subject('senegal'))
#count_tweets('ASMOL')