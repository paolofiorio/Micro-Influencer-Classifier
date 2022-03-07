import pandas as pd
import csv
import os


df1 = pd.read_csv('users_tweets_percentages.csv')

df = df1.loc[df1['micro'] == 1]

scores = []

for i in range(0,len(df1['id'])):
  score=0
  #score by followers
  if(5000<=df1['followers'].iloc[i]<=df['followers'].quantile(0.2)):
    score+=2
  elif(df['followers'].quantile(0.2)<df1['followers'].iloc[i]<=df['followers'].quantile(0.4)):
    score+=4
  elif(df['followers'].quantile(0.4)<df1['followers'].iloc[i]<=df['followers'].quantile(0.6)):
    score+=6
  elif(df['followers'].quantile(0.6)<df1['followers'].iloc[i]<=df['followers'].quantile(0.8)):
    score+=8
  elif(df['followers'].quantile(0.8)<df1['followers'].iloc[i]<=100000):
    score+=10

  #score by followers growth rate
  if(4<=df1['followers_growth_rate'].iloc[i]<=df['followers_growth_rate'].quantile(0.2)):
    score+=2
  elif(df['followers_growth_rate'].quantile(0.2)<df1['followers_growth_rate'].iloc[i]<=df['followers_growth_rate'].quantile(0.4)):
    score+=4
  elif(df['followers_growth_rate'].quantile(0.4)<df1['followers_growth_rate'].iloc[i]<=df['followers_growth_rate'].quantile(0.6)):
    score+=6
  elif(df['followers_growth_rate'].quantile(0.6)<df1['followers_growth_rate'].iloc[i]<=df['followers_growth_rate'].quantile(0.8)):
    score+=8
  elif(df1['followers_growth_rate'].iloc[i]>df['followers_growth_rate'].quantile(0.8)):
    score+=10

  #score by followers following ratio
  if(2<=df1['followers_following_ratio'].iloc[i]<=df['followers__following_ratio'].quantile(0.2)):
    score+=2
  elif(df['followers__following_ratio'].quantile(0.2)<df1['followers_following_ratio'].iloc[i]<=df['followers__following_ratio'].quantile(0.4)):
    score+=4
  elif(df['followers__following_ratio'].quantile(0.4)<df1['followers_following_ratio'].iloc[i]<=df['followers__following_ratio'].quantile(0.6)):
    score+=6
  elif(df['followers__following_ratio'].quantile(0.6)<df1['followers_following_ratio'].iloc[i]<=df['followers__following_ratio'].quantile(0.8)):
    score+=8
  elif(df1['followers_following_ratio'].iloc[i]>df['followers__following_ratio'].quantile(0.8)):
    score+=10
  
  #score by tweet frequency
  if(10<=df1['tweet_freq'].iloc[i]<=df['tweet_freq'].quantile(0.2)):
    score+=2
  elif(df['tweet_freq'].quantile(0.2)<df1['tweet_freq'].iloc[i]<=df['tweet_freq'].quantile(0.4)):
    score+=4
  elif(df['tweet_freq'].quantile(0.4)<df1['tweet_freq'].iloc[i]<=df['tweet_freq'].quantile(0.6)):
    score+=6
  elif(df['tweet_freq'].quantile(0.6)<df1['tweet_freq'].iloc[i]<=df['tweet_freq'].quantile(0.8)):
    score+=8
  elif(df1['tweet_freq'].iloc[i]>df['tweet_freq'].quantile(0.8)):
    score+=10

  #score by interactions
  if(0<=df1['interactions_no_retweets'].iloc[i]<=df['interactions_no_retweets'].quantile(0.2)):
    score+=2
  elif(df['interactions_no_retweets'].quantile(0.2)<df1['interactions_no_retweets'].iloc[i]<=df['interactions_no_retweets'].quantile(0.4)):
    score+=4
  elif(df['interactions_no_retweets'].quantile(0.4)<df1['interactions_no_retweets'].iloc[i]<=df['interactions_no_retweets'].quantile(0.6)):
    score+=6
  elif(df['interactions_no_retweets'].quantile(0.6)<df1['interactions_no_retweets'].iloc[i]<=df['interactions_no_retweets'].quantile(0.8)):
    score+=8
  elif(df1['interactions_no_retweets'].iloc[i]>df['interactions_no_retweets'].quantile(0.8)):
    score+=10

  #score by topic % in tweets
  if(0<=df1['topicInTweetsPercentage'].iloc[i]<=df['topicInTweetsPercentage'].quantile(0.2)):
    score+=5
  elif(df['topicInTweetsPercentage'].quantile(0.2)<df1['topicInTweetsPercentage'].iloc[i]<=df['topicInTweetsPercentage'].quantile(0.4)):
    score+=10
  elif(df['topicInTweetsPercentage'].quantile(0.4)<df1['topicInTweetsPercentage'].iloc[i]<=df['topicInTweetsPercentage'].quantile(0.6)):
    score+=15
  elif(df['topicInTweetsPercentage'].quantile(0.6)<df1['topicInTweetsPercentage'].iloc[i]<=df['topicInTweetsPercentage'].quantile(0.8)):
    score+=20
  elif(df1['topicInTweetsPercentage'].iloc[i]>df['topicInTweetsPercentage'].quantile(0.8)):
    score+=25

  #score by topic % in words
  if(0<=df1['topicInWordsPercentage'].iloc[i]<=df['topicInWordsPercentage'].quantile(0.2)):
    score+=5
  elif(df['topicInWordsPercentage'].quantile(0.2)<df1['topicInWordsPercentage'].iloc[i]<=df['topicInWordsPercentage'].quantile(0.4)):
    score+=10
  elif(df['topicInWordsPercentage'].quantile(0.4)<df1['topicInWordsPercentage'].iloc[i]<=df['topicInWordsPercentage'].quantile(0.6)):
    score+=15
  elif(df['topicInWordsPercentage'].quantile(0.6)<df1['topicInWordsPercentage'].iloc[i]<=df['topicInWordsPercentage'].quantile(0.8)):
    score+=20
  elif(df1['topicInWordsPercentage'].iloc[i]>df['topicInWordsPercentage'].quantile(0.8)):
    score+=25

  scores.append(score)
 


cols = df1.columns.tolist()
df1.insert(len(cols),"scores", scores)


df1= df1.sort_values(by=['topic','micro','scores'],ascending=False)
dfFinal= df1.drop(columns=['id','tweet','age','followers','tweet_freq','followers_growth_rate','followers_following_ratio','interactions_no_retweets','topicInTweetsPercentage', 'topicInWordsPercentage' ])
print(dfFinal.head())
dfFinal.to_csv('rankings.csv', encoding='UTF8',index=False)
print("Rankings dataset created")
