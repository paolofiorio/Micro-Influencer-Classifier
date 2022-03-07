import numpy as np
import tweepy
import datetime
import pandas as pd
from langdetect import detect
import stopwordsiso as stopwords
from emoji import demojize
from nltk.stem.wordnet import WordNetLemmatizer
import re
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax
import pickle 
import argparse

#get models, insert their names

Pkl1_Filename = "./Pickle_XGB_Model.pkl"  
with open(Pkl1_Filename, 'rb') as file: 
    Pickled_XGB_Model = pickle.load(file)
    
Pkl2_Filename = "./Pickle_XGB_ModelMicroTopic.pkl"  
with open(Pkl2_Filename, 'rb') as file:  
    Pickled_XGB_ModelMicroTopic = pickle.load(file)
    
tokenizer = AutoTokenizer.from_pretrained("cardiffnlp/twitter-roberta-base-sentiment")
model = AutoModelForSequenceClassification.from_pretrained("cardiffnlp/twitter-roberta-base-sentiment")
model.save_pretrained("cardiffnlp/twitter-roberta-base-sentiment")


#class to store users
class User:
    def __init__(self, id,screen_name,followers,age,followers_growth_rate,followers_following_ratio,tweet_freq, topic, pos,neu,neg):
        self.id=id
        self.screen_name = screen_name
        self.age=age
        self.followers = followers
        self.followers_growth_rate=followers_growth_rate
        self.followers_following_ratio = followers_following_ratio
        self.tweet_freq = tweet_freq
        self.topic = topic
        self.pos = pos
        self.neu=neu
        self.neg = neg
    
#evaluate age in days
def evaluate_user_age(creation):
	age=0
	now = datetime.datetime.now()
	ci = creation.strftime("%Y-%m-%d %H:%M:%S")
	c= datetime.datetime.strptime(ci, "%Y-%m-%d %H:%M:%S")
	age = ((now-c).total_seconds())/(3600*24) #age in days
	return age


#obtain most common language
def most_common(lst):
    return max(set(lst), key=lst.count)

#clean tweet
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
    return temp


#Twitter access, insert here your credentials
consumer_key = ''
consumer_secret = ''
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
api = tweepy.API(auth)

parser = argparse.ArgumentParser()
parser.add_argument('--users', help='users list input', type=str, required=True)
parser.add_argument('--topic', help='topic input', type=str, required = True)
args = parser.parse_args()
users= [str(item) for item in args.users.split(',')]
topic = args.topic

#useful lists
#users = ["ADDiane", "LanaToro21"]
#topic ="sustainability"
language = ["en"]
users_returned = []
users_id = []
indexesL = []
followersL=[]
ageL=[]
followers_growth_rateL=[]
followers_following_ratioL=[]
tweet_freqL=[]
tweetsPercentageL=[]
wordsPercentageL=[]
interactionsL=[]
userLanguageL=[]
positiveL=[]
neutralL=[]
negativeL=[]
print("Users stats retrieval..")

for name in users:
    #counters and tweets for each user
    count =0
    interactions=0
    tweets=[]
    u = api.get_user(screen_name = name)
    idx = u.id
    indexesL.append(idx)
    age = evaluate_user_age(u.created_at)
    ageL.append(age)
    followersL.append(u.followers_count)
    followers_growth_rate = u.followers_count/age
    followers_growth_rateL.append(followers_growth_rate)
    followers_following_ratio = u.followers_count/(u.friends_count+1)
    followers_following_ratioL.append(followers_following_ratio)
    tweet_freq = u.statuses_count/age
    tweet_freqL.append(tweet_freq)
    
    for status in tweepy.Cursor(api.user_timeline,user_id=u.id,
                                        tweet_mode="extended").items():
            if(count<100):
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
                tweets.append(status.full_text.replace('\n',' '))
                count+=1
            else: break;

    interactionsL.append(interactions)

    #clean tweets, search topic % and evaluate sentiment

    #counters
    t=0 #tweets
    f=0 #topics found
    wo=0 #words
    langs=[]
    lis = []

    labels = ['negative', 'neutral', 'positive']  
    pos =[]
    neu=[]
    neg=[]
    #for each tweet
    for twit in tweets:
        for tw in twit.split("', "):
            #another split because replies use " instead of '
            for tweet in tw.split('", '):
                #flag to avoid multiple topics written in the same tweet
                found = False 
                #increase tweets counter
                t+=1

                #evaluate tweet language (subset) every 20
                if (t%20==0):
                    try:
                        language = detect(tweet)
                    except:
                        language = "Not available"
                
                    langs.append(language)

                #for each word
                for w in tweet.split(" "):
                    #count how many times the topic is written
                    if (topic.lower() in w.lower() and found==False):
                        f+=1
                        found=True
                    #increase words counter
                    wo+=1

                cleann = clean_tweet(tweet)
                for k in cleann:
                    encoded_input = tokenizer(k, return_tensors='pt')
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
        
    #evaluate how many times the topic is written inside tweets
    #print(f, "topic word over",t, "tweets with", wo, "total words")
    percT = ((f)/t)*100
    tweetsPercentageL.append(percT)

    #evaluate percentage of word topic written with respect to all words
    percW = ((f)/wo)*100
    wordsPercentageL.append(percW)
    #print("Percentage of topic", topic," in tweets = ", percT, "%")
    #print("Percentage of topic", topic," in words = ", percW, "%")
    
    #evaluate most common language for the user
    finalLanguage = most_common(langs)
    userLanguageL.append(finalLanguage)
    
    #create user object
    m = User(u.id, u.screen_name, u.followers_count, age, followers_growth_rate,
                                    followers_following_ratio, tweet_freq, topic,np.mean(pos),np.mean(neu),np.mean(neg))
    users_returned.append(m)
    users_id.append(u.id)
    positiveL.append(np.mean(pos))
    neutralL.append(np.mean(neu))
    negativeL.append(np.mean(neg))


#create dataframe
df = pd.DataFrame()
df['id'] = indexesL
df['language'] = userLanguageL
df['followers']= followersL
df['age']=ageL
df['followers_growth_rate']=followers_growth_rateL
df['followers_following_ratio']= followers_following_ratioL
df['tweet_freq']= tweet_freqL
df['interactions_no_retweets']= interactionsL
df['topicInTweetsPercentage']=tweetsPercentageL
df['topicInWordsPercentage'] = wordsPercentageL
df['positiveSentiment'] =positiveL
df['neutralSentiment']= neutralL
df['negativeSentiment']=negativeL


X = df.loc[:, ["followers", "age", "followers_growth_rate", "followers_following_ratio", "tweet_freq","interactions_no_retweets","topicInTweetsPercentage", "topicInWordsPercentage", 
"positiveSentiment","neutralSentiment" ,"negativeSentiment"]]
X = X.to_numpy()

#predict
Ypredict = Pickled_XGB_Model.predict(X)
YpredictMicroTopic = Pickled_XGB_ModelMicroTopic.predict(X) 


for i in range(len(users)):
    if(Ypredict[i]==1):
        print(users[i],"is a microinfluencer")
    else:
        print(users[i],"is NOT a microinfluencer")
    
    if(YpredictMicroTopic[i]==1):
        print(users[i],"is a microinfluencer for the topic", topic)
    else:
        print(users[i],"is NOT a microinfluencer for the topic", topic)
