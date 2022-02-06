import requests
from tween.credentials import TOKEN
import json
import pandas as pd
import plotly.express as px

def count_tweets(key_value: str):
  key_value = key_value.replace(' ', '%20')
  key_value = key_value.replace('#', '%23')

  url = f"https://api.twitter.com/2/tweets/counts/recent?query={key_value}&granularity=hour"

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

count_tweets('ASMOL')