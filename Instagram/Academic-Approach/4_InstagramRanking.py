import pandas as pd
import numpy as np

df = pd.read_csv("usersInstagramPercentages.csv")

df1 =df.loc[df['micro']==1] #only micro influencers dataset to evaluate their percentiles

scores = []

for i in range(0,len(df['id'])):
  score=0
  #score by followers
  if(5000<=df['followers'].iloc[i]<=df1['followers'].quantile(0.2)):
    score+=2.5
  elif(df1['followers'].quantile(0.2)<df['followers'].iloc[i]<=df1['followers'].quantile(0.4)):
    score+=5
  elif(df1['followers'].quantile(0.4)<df['followers'].iloc[i]<=df1['followers'].quantile(0.6)):
    score+=7.5
  elif(df1['followers'].quantile(0.6)<df['followers'].iloc[i]<=df1['followers'].quantile(0.8)):
    score+=10
  elif(df1['followers'].quantile(0.8)<df['followers'].iloc[i]<=100000):
    score+=12.5

  #score by followers following ratio
  if(2<=df['followers_following_ratio'].iloc[i]<=df1['followers_following_ratio'].quantile(0.2)):
    score+=2.5
  elif(df1['followers_following_ratio'].quantile(0.2)<df['followers_following_ratio'].iloc[i]<=df1['followers_following_ratio'].quantile(0.4)):
    score+=5
  elif(df1['followers_following_ratio'].quantile(0.4)<df['followers_following_ratio'].iloc[i]<=df1['followers_following_ratio'].quantile(0.6)):
    score+=7.5
  elif(df1['followers_following_ratio'].quantile(0.6)<df['followers_following_ratio'].iloc[i]<=df1['followers_following_ratio'].quantile(0.8)):
    score+=10
  elif(df['followers_following_ratio'].iloc[i]>df1['followers_following_ratio'].quantile(0.8)):
    score+=12.5

  #score by followers per media
  if(2<=df['followers_per_media'].iloc[i]<=df1['followers_per_media'].quantile(0.2)):
    score+=2.5
  elif(df1['followers_per_media'].quantile(0.2)<df['followers_per_media'].iloc[i]<=df1['followers_per_media'].quantile(0.4)):
    score+=5
  elif(df1['followers_per_media'].quantile(0.4)<df['followers_per_media'].iloc[i]<=df1['followers_per_media'].quantile(0.6)):
    score+=7.5
  elif(df1['followers_per_media'].quantile(0.6)<df['followers_per_media'].iloc[i]<=df1['followers_per_media'].quantile(0.8)):
    score+=10
  elif(df['followers_per_media'].iloc[i]>df1['followers_per_media'].quantile(0.8)):
    score+=12.5

  #score by interactions
  if(0<=df['interactions'].iloc[i]<=df1['interactions'].quantile(0.2)):
    score+=2.5
  elif(df1['interactions'].quantile(0.2)<df['interactions'].iloc[i]<=df1['interactions'].quantile(0.4)):
    score+=5
  elif(df1['interactions'].quantile(0.4)<df['interactions'].iloc[i]<=df1['interactions'].quantile(0.6)):
    score+=7.5
  elif(df1['interactions'].quantile(0.6)<df['interactions'].iloc[i]<=df1['interactions'].quantile(0.8)):
    score+=10
  elif(df['interactions'].iloc[i]>df1['interactions'].quantile(0.8)):
    score+=12.5

  #score by topic % in captions
  if(0<=df['topicInCaptionsPercentage'].iloc[i]<=df1['topicInCaptionsPercentage'].quantile(0.2)):
    score+=2.5
  elif(df1['topicInCaptionsPercentage'].quantile(0.2)<df['topicInCaptionsPercentage'].iloc[i]<=df1['topicInCaptionsPercentage'].quantile(0.4)):
    score+=5
  elif(df1['topicInCaptionsPercentage'].quantile(0.4)<df['topicInCaptionsPercentage'].iloc[i]<=df1['topicInCaptionsPercentage'].quantile(0.6)):
    score+=7.5
  elif(df1['topicInCaptionsPercentage'].quantile(0.6)<df['topicInCaptionsPercentage'].iloc[i]<=df1['topicInCaptionsPercentage'].quantile(0.8)):
    score+=10
  elif(df['topicInCaptionsPercentage'].iloc[i]>df1['topicInCaptionsPercentage'].quantile(0.8)):
    score+=12.5

  #score by topic % in words
  if(0<=df['topicInWordsPercentage'].iloc[i]<=df1['topicInWordsPercentage'].quantile(0.2)):
    score+=2.5
  elif(df1['topicInWordsPercentage'].quantile(0.2)<df['topicInWordsPercentage'].iloc[i]<=df1['topicInWordsPercentage'].quantile(0.4)):
    score+=5
  elif(df1['topicInWordsPercentage'].quantile(0.4)<df['topicInWordsPercentage'].iloc[i]<=df1['topicInWordsPercentage'].quantile(0.6)):
    score+=7.5
  elif(df1['topicInWordsPercentage'].quantile(0.6)<df['topicInWordsPercentage'].iloc[i]<=df1['topicInWordsPercentage'].quantile(0.8)):
    score+=10
  elif(df['topicInWordsPercentage'].iloc[i]>df1['topicInWordsPercentage'].quantile(0.8)):
    score+=12.5

  #score by topic % in pics
  if(0<=df['topicInPicsPercentage'].iloc[i]<=df1['topicInPicsPercentage'].quantile(0.92)):
    score+=2.5
  elif(df1['topicInPicsPercentage'].quantile(0.92)<df['topicInPicsPercentage'].iloc[i]<=df1['topicInPicsPercentage'].quantile(0.94)):
    score+=5
  elif(df1['topicInPicsPercentage'].quantile(0.94)<df['topicInPicsPercentage'].iloc[i]<=df1['topicInPicsPercentage'].quantile(0.96)):
    score+=7.5
  elif(df1['topicInPicsPercentage'].quantile(0.96)<df['topicInPicsPercentage'].iloc[i]<=df1['topicInPicsPercentage'].quantile(0.98)):
    score+=10
  elif(df['topicInPicsPercentage'].iloc[i]>df1['topicInPicsPercentage'].quantile(0.98)):
    score+=12.5

  #score by topic % in pics
  if(0<=df['topicInPicsWordsPercentage'].iloc[i]<=df1['topicInPicsWordsPercentage'].quantile(0.92)):
    score+=2.5
  elif(df1['topicInPicsWordsPercentage'].quantile(0.92)<df['topicInPicsWordsPercentage'].iloc[i]<=df1['topicInPicsWordsPercentage'].quantile(0.94)):
    score+=5
  elif(df1['topicInPicsWordsPercentage'].quantile(0.94)<df['topicInPicsWordsPercentage'].iloc[i]<=df1['topicInPicsWordsPercentage'].quantile(0.96)):
    score+=7.5
  elif(df1['topicInPicsWordsPercentage'].quantile(0.96)<df['topicInPicsWordsPercentage'].iloc[i]<=df1['topicInPicsWordsPercentage'].quantile(0.98)):
    score+=10
  elif(df['topicInPicsWordsPercentage'].iloc[i]>df1['topicInPicsWordsPercentage'].quantile(0.98)):
    score+=12.5

  scores.append(score)

df['scores']= scores

half = df['scores'].quantile(0.5)
print(half)
df['microTopic'] = np.where(df['scores']>=half, 1, 0) #assign micrro topic to 1 if the score overcomes the 0.5 percentile of the scores' column


df.to_csv('usersInstagramMicroTopicCC.csv', encoding='UTF8',index=False)
print("Rankings dataset created")
