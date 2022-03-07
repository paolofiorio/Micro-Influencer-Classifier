import csv
import pandas as pd
import langdetect
from langdetect import detect


#obtain most common language
def most_common(lst):
    return max(set(lst), key=lst.count)



#open file with users, use pandas as alternative
with open('users_tweets.csv', newline='',encoding='UTF8' ) as f:
    reader = csv.reader(f)
    next(reader, None)  # skip the headers
    users = list(reader)

#get users ids
ids = []
topic = []
tweets = []

for u in users:
    ids.append(u[0])
    topic.append(u[8])
    tweets.append(u[9])


print("Evaluating topic presence and language...")
tweetsPercentage=[]
wordsPercentage=[]
userLanguage=[]
for i in range(0,len(ids)):
    #counters
    t=0 #tweets
    f=0 #topics found
    wo=0 #words
    langs=[]
    #for each tweet
    for tw in tweets[i].split("', "):
        #another split because replies use " instead of '
        for tweet in tw.split('", '):
            #flag to avoid multiple topics written in the same tweet
            found = False 
         
            #increase number of tweets
            t+=1

            #evaluate tweet language (subset)
            if (t%20==0):
                try:
                    language = detect(tweet)
                except:
                    language = "Not available"
            
                langs.append(language)

            
            #for each word
            for w in tweet.split(" "):
                #count how many times the topic is written
                if (topic[i].lower() in w.lower() and found==False):
                    f+=1
                    found=True
                #increase number of words
                wo+=1
    #evaluate how many times the topic is written inside tweets
    print(f, "topic word over",t, "tweets with", wo, "total words")
    percT = ((f)/t)*100
    #evaluate percentage of word topic written with respect to all words
    percW = ((f)/wo)*100
    print("Percentage of topic", topic[i]," in tweets = ", percT, "%")
    print("Percentage of topic", topic[i]," in words = ", percW, "%")
    #evaluate most common language for the user
    finalLanguage = most_common(langs)
    print(finalLanguage)
    print("\n")

    tweetsPercentage.append(percT)
    wordsPercentage.append(percW)
    userLanguage.append(finalLanguage)
    



#create new datasets by adding topic percentages for both tweets and words in the original datasets
df = pd.read_csv('users_tweetsLarge.csv')
df['topicInTweetsPercentage']= tweetsPercentage
df['topicInWordsPercentage']= wordsPercentage
df['language']= userLanguage
print(df.head())
df.to_csv('users_tweets_percentages.csv', encoding='UTF8',index=False)

print("Users_tweets_percentages dataset created")
