import pandas as pd
import instaloader
from instaloader import Instaloader
import argparse


#insert your Instagram's credentials
USER = ""
PASSWORD = ""
L = Instaloader()
L.login(USER, PASSWORD)

#pass as argument list of users and topic of interest
parser = argparse.ArgumentParser()
parser.add_argument('--users', help='users list input', type=str, required=True)
parser.add_argument('--topic', help='topic input', type=str, required = True)
args = parser.parse_args()
users= [str(item) for item in args.users.split(',')]
topic = args.topic

#lists
users_id=[]
usernames = []
followers = []
followers_following_ratios = []
followers_per_media = []
captions = []
urls=[]
interactions =[]
topics=[]

for name in users:
    p=0 #posts counter
    inter = 0 #interactions counter
    caps = [] #list for each post caption
    ur = [] #list for each image url
    profile = instaloader.Profile.from_username(L.context, name)
    users_id.append(profile.userid)
    usernames.append(profile.username)
    followers.append(profile.followers)
    followers_per_media.append(profile.followers/profile.mediacount)
    followers_following_ratios.append((profile.followers+1)/(profile.followees+1))
    topics.append(topic)
    for post in profile.get_posts():
        if(post.typename != "GraphVideo"): #avoid videos
            k = str(post.caption)+ " "
            k = k.replace('\n', " ")
            caps.append(k)
            ur.append(post.url)
            inter+=post.likes + post.comments #increase interactions
            p+=1 #increase number of posts until 25 is reached
        if(p==25): break;
    interactions.append(inter)
    urls.append(ur)
    captions.append(caps)

#create input dataset
df = pd.DataFrame()
df['id']= users_id
df['username']= usernames
df['followers']= followers
df['followers_per_media']= followers_per_media
df['followers_following_ratio']=followers_following_ratios
df['captions']=captions
df['urls']=urls
df['interactions']=interactions
df['topic']= topics

print(df)

df.to_csv('InputInstagram.csv', encoding='UTF8',index=False)
print("Users Input dataset created")
