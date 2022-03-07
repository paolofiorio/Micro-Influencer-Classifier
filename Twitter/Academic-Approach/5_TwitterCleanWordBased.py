import pandas as pd
import csv
import os
import nltk
from langdetect import detect
from langdetect import detect_langs
import numpy as np
import re
import stopwordsiso as stopwords
import emoji
from emoji import demojize
from nltk.stem.wordnet import WordNetLemmatizer


df1 = pd.read_csv('users_tweets_percentages.csv')
df2 = pd.read_csv('rankingsLarge.csv')
df2 = df2.drop(columns=['micro','topic','language'])
df = df1.merge(df2, on='screen_name', left_index=False)

half = df['scores'].quantile(0.5)

#nlp word based
def clean_tweet(tweet):
    try:
        language = detect(tweet)
    except:
        language = "Not available"

    if(stopwords.has_lang(language)):
      stop = stopwords.stopwords(language)
    else:
      stop = stopwords.stopwords("en")

    tweet = demojize(tweet) #convert emojis to text
    temp = tweet.lower()
    temp = re.sub("'", "", temp) # to avoid removing contractions in english
    temp = re.sub("@[A-Za-z0-9_]+","", temp) #remove entire tag (@ and also name tagged)
    temp = re.sub("#","", temp) #remove only hashtag symbol
    temp = re.sub(r'http\S+', '', temp)  #remove links
    temp = re.sub('[()!?.,;:]', ' ', temp) #remove ()!?.,:;
    temp = re.sub('\[.*\].*',' ', temp) #remove []
    #temp = re.sub("[^a-z0-9]"," ", temp)
    temp = re.sub("[^a-z]"," ", temp) #remove numbers
    temp = temp.split()
    temp = [w for w in temp if not w in stop]
    temp = [WordNetLemmatizer().lemmatize(w, pos='v') for w in temp] #not for sentence based
    return temp

tweets = df['tweet']
all=[]
for j in range(0,len(df['id'])):
  lis= []
  for tw in tweets[j].split("', "):
      #another split because replies use " instead of '
      for tweet in tw.split('", '):
        t = clean_tweet(tweet)
        
        for k in t:
          lis.append(k)
        
  all.append(lis)
  

dfFinal = pd.DataFrame()
dfFinal['id'] = df['id']
dfFinal['screen_name'] = df['screen_name']
dfFinal['topic'] = df['topic']
dfFinal['language'] = df['language']
dfFinal['scores']= df['scores']
dfFinal['microTopic'] = np.where(df['scores']>=half, 1, 0)
dfFinal['micro'] = df['micro']
dfFinal['tweets'] = all

dfFinal.to_csv('cleanWordBased.csv', encoding='UTF8',index=False)
print(dfFinal.head())
