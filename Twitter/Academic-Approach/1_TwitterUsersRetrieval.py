import tweepy
import datetime
import csv
import time

#class to store users
class User:
    def __init__(self, id,screen_name,followers,age,followers_growth_rate,followers_following_ratio,tweet_freq,micro, topic):
        self.id=id
        self.screen_name = screen_name
        self.age=age
        self.followers = followers
        self.followers_growth_rate=followers_growth_rate
        self.followers_following_ratio = followers_following_ratio
        self.tweet_freq = tweet_freq
        self.micro = micro
        self.topic = topic
    
#evaluate age in days
def evaluate_user_age(creation):
	age=0
	now = datetime.datetime.now()
	ci = creation.strftime("%Y-%m-%d %H:%M:%S")
	c= datetime.datetime.strptime(ci, "%Y-%m-%d %H:%M:%S")
	age = ((now-c).total_seconds())/(3600*24) #age in days
	return age

#Twitter access, insert here your credentials
consumer_key = ''
consumer_secret = ''
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
api = tweepy.API(auth)

#useful lists
users_returned = []
users_id = [] #list to store ids and avoid duplicates
topics =[] #insert here the topics of your interest
languages = [] #insert here the languages of your interest
print("Users retrieval..")

#for each topic
for topic_selected in topics:
    #counters for micro and not micro
    micro =0
    not_micro =0
    
    #for each language
    for l in languages:
        #selecting in this case 5 micro and 5 not micro
        try:
            while(micro<5 or not_micro<5):
            #get last tweets about the given topic
                
            
                for tweet in tweepy.Cursor(api.search_tweets, q=topic_selected, count=100, lang=l).items(800):
                    #get tweet's user
                    u = tweet.user
                    #evaluate some info about the user
                    age = evaluate_user_age(u.created_at)
                    followers_growth_rate = u.followers_count/age
                    followers_following_ratio = u.followers_count/(u.friends_count+1)
                    tweet_freq = u.statuses_count/age
                    #check if user may be microinfluencer
                    if (u.verified == False and u.followers_count > 5000 and u.followers_count < 100000 and followers_growth_rate > 4 and followers_following_ratio > 2 and tweet_freq > 10 and u.statuses_count>200):
                        #if still less than 5 found and is not already present
                        if(micro < 5 and u.id not in users_id):
                            #create user object, increase counter and store
                            m = User(u.id, u.screen_name, u.followers_count, age, followers_growth_rate,
                                    followers_following_ratio, tweet_freq, 1, topic_selected)
                            micro += 1
                            users_returned.append(m)
                            users_id.append(u.id)
                    else:
                        if(tweet_freq > 10 and u.statuses_count>200):
                            #user is not a microinfluencer, store 5 uniques
                            if(not_micro < 5 and u.id not in users_id):
                                #create user object, increase counter and store
                                m = User(u.id, u.screen_name, u.followers_count, age, followers_growth_rate,
                                        followers_following_ratio, tweet_freq, 0, topic_selected)
                                not_micro += 1        
                                users_returned.append(m)
                                users_id.append(u.id)
            
        except tweepy.TooManyRequests:
            time.sleep(15*60)


#for us in users_returned:
    #print(us.screen_name, us.topic, us.micro)
    
users = ([us.id, us.screen_name, us.followers, us.age, us.followers_growth_rate, us.followers_following_ratio, us.tweet_freq, us.micro, us.topic] for us in users_returned)


#write csv file with all users info, 0 or 1 for not micro or microinfluencer, topic
header = ["id","screen_name","followers","age","followers_growth_rate","followers_following_ratio","tweet_freq","micro", "topic"]
with open('users.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)

    # write the header
    writer.writerow(header)

    # write the data
    writer.writerows(u for u in users)
    
print("Users dataset created")
