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
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax

tokenizer = AutoTokenizer.from_pretrained("cardiffnlp/twitter-roberta-base-sentiment")

model = AutoModelForSequenceClassification.from_pretrained("cardiffnlp/twitter-roberta-base-sentiment")

model.save_pretrained("cardiffnlp/twitter-roberta-base-sentiment")



df1 = pd.read_csv('users_tweets_percentages.csv')
df2 = pd.read_csv('rankings.csv')
df2 = df2.drop(columns=['micro','topic','language'])
df = df1.merge(df2, on='screen_name', left_index=False)

half = df['scores'].quantile(0.5)

#nlp to clean tweets
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
    temp = re.sub("[^a-z]"," ", temp) #remove numbers
    temp = temp.split()
    temp = [w for w in temp if not w in stop]
    temp = [WordNetLemmatizer().lemmatize(w, pos='v') for w in temp] #not for sentence based
    temp = " ".join(word for word in temp)
    return temp

tweets = df['tweet']

all=[]
positiveSentiment=[]
neutralSentiment=[]
negativeSentiment=[]
labels = ['negative', 'neutral', 'positive']
for j in range(0,len(df['id'])):
  lis= []
  pos =[]
  neu=[]
  neg=[]
  for tw in tweets[j].split("', "):
      #another split because replies use " instead of '
      for tweet in tw.split('", '):
        t = clean_tweet(tweet)
        lis.append(t)
        encoded_input = tokenizer(t, return_tensors='pt')
        output = model(**encoded_input)
        scores = output[0][0].detach().numpy()
        scores = softmax(scores)

        ranking = np.argsort(scores)
        ranking = ranking[::-1]
        for i in range(scores.shape[0]):
            l = labels[ranking[i]]
            s = scores[ranking[i]]
            if(l=='positive'):
                pos.append(s)
            elif(l=='neutral'):
                neu.append(s)
            else:
                neg.append(s)
        
  all.append(lis)
  positiveSentiment.append(np.mean(pos))
  neutralSentiment.append(np.mean(neu))
  negativeSentiment.append(np.mean(neg))

  

dfFinal = pd.DataFrame()
dfFinal['id'] = df['id']
dfFinal['screen_name'] = df['screen_name']
dfFinal['followers'] = df['followers']
dfFinal['age'] = df['age']
dfFinal['followers_growth_rate'] = df['followers_growth_rate']
dfFinal['followers_following_ratio'] = df['followers_following_ratio']
dfFinal['tweet_freq'] = df['tweet_freq']
dfFinal['interactions_no_retweets'] = df['interactions_no_retweets']
dfFinal['topicInTweetsPercentage'] = df['topicInTweetsPercentage']
dfFinal['topicInWordsPercentage'] = df['topicInWordsPercentage']
dfFinal['topic'] = df['topic']
dfFinal['language'] = df['language']
dfFinal['scores']= df['scores']
dfFinal['microTopic'] = np.where(df['scores']>=half, 1, 0)
dfFinal['micro'] = df['micro']
dfFinal['positiveSentiment']=positiveSentiment
dfFinal['neutralSentiment']=neutralSentiment
dfFinal['negativeSentiment']=negativeSentiment
dfFinal['tweets'] = all

dfFinal.to_csv('cleanTweetsSentiment.csv', encoding='UTF8',index=False)
print(dfFinal.head())
