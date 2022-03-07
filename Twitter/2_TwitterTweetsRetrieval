import tweepy
import csv
import time
import pandas as pd

#Twitter access, insert your credentials
consumer_key = ''
consumer_secret = ''
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
api = tweepy.API(auth)

#open file with users, use pandas library in alternative
with open('users.csv', newline='') as f:
    reader = csv.reader(f)
    next(reader, None)  # skip the headers
    users = list(reader)

#get users ids
ids = []
for u in users:
    ids.append(u[0])

user_tweets =[]
for i in ids:
    all_tweets = []
    interactions=0
    count =0
    try:
        for status in tweepy.Cursor(api.user_timeline,user_id=i,
                                        tweet_mode="extended").items():
            if(count<200):
              
                #add interactions only for tweets, not for retweets because twitter counts original retweets and likes
                if (status.full_text.startswith("RT @") is True):
                    interactions+= 0
                else :
                    interactions+= status.retweet_count+status.favorite_count
                if (status.full_text.startswith("RT @") is True):
                    try:
                        status = status.retweeted_status
                    except:
                        status = status

                all_tweets.append(status.full_text.replace('\n',' '))
                count+=1
            else: break;
    except tweepy.TooManyRequests:
            time.sleep(15*60)
    user_tweets.append([i,all_tweets,interactions])



#create csv
header = ["id","tweet", "interactions_no_retweets"]


with open('tweets.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)

    # write the header
    writer.writerow(header)

    # write the data
    writer.writerows(u for u in user_tweets)
    
print("Tweets dataset created")




df1 = pd.read_csv('users.csv')
df2 = pd.read_csv('tweets.csv')

df = df1.merge(df2, on='id', left_index=False)

df.to_csv('users_tweets.csv', encoding='UTF8',index=False)
print("Users_tweets dataset created")
