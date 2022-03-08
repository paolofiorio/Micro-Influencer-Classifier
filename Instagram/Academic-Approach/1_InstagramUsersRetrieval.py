import pandas as pd
import instaloader
from instaloader import Instaloader

#insert credentials of your Instagram account
USER = ""
PASSWORD = ""
L = Instaloader()
L.login(USER, PASSWORD)

# Custom function to extract various attributes given a hashtag
def scraper(tags,L):
  #lists to store each parameter
  users_id=[]
  caption = []
  username = []
  following = []
  followersL = []
  followers_per_media=[]
  ratio = []
  urls=[]
  interactions =[]
  ismicro = []
  topics=[]
  for hashtag in tags:
    #counters
    micro =0
    not_micro =0
    
    for i in instaloader.Hashtag.from_name(L.context, hashtag).get_top_posts():
      if(micro==5 and not_micro ==5):
          break;
      if (i.is_video==False): #avoid videos
        profile = instaloader.Profile.from_username(L.context, i.owner_username)
        mediacount = profile.mediacount
        uid = profile.userid
        followers = profile.followers
        followers_following_ratio = (profile.followers+1)/(profile.followees+1)
        f_per_media = profile.followers / profile.mediacount
        
        #counters for posts and interactions, lists to store captions and urls of each post
        p=0
        inter =0
        ur=[]
        captions = []
        p1=0
        inter1 =0
        ur1=[]
        captions1 = []
        
        #parameters to select micro influencers 
        if(followers>5000 and followers<100000 and followers_following_ratio>2 and f_per_media>2 and mediacount>200):
          if(micro==5 and not_micro ==5):
            break;
          if(micro<5 and uid not in users_id):        
            for post in profile.get_posts(): #last posts
                if(post.typename != "GraphVideo"): #avoid videos
                    k = str(post.caption)+ " "
                    k = k.replace('\n', " ") #avoid \n
                    captions.append(k)
                    ur.append(post.url)
                    inter+=post.likes + post.comments #increase interactions
                    p+=1 #increase number of posts until 25 is reached
                if(p==25): break;
            users_id.append(uid)
            username.append(i.owner_username)
            following.append(profile.followees)
            followersL.append(profile.followers)
            followers_per_media.append(f_per_media)
            ratio.append(followers_following_ratio)
            ismicro.append(1)
            topics.append(hashtag)
            micro+=1
              
            interactions.append(inter)
            urls.append(ur)
            caption.append(captions)
        #selection of not micro influencers
        else:
          if(mediacount>200 and (followers<5000 or followers>100000)):
            if(not_micro<5 and uid not in users_id):
              for post in profile.get_posts(): #last posts
                  if(post.typename != "GraphVideo"):
                      k = str(post.caption)+ " "
                      k = k.replace('\n', " ")
                      captions1.append(k)
                      ur1.append(post.url)
                      inter1+=post.likes + post.comments
                      p1+=1
                  if(p1==25): break;
              users_id.append(uid)
              username.append(i.owner_username)
              following.append(profile.followees)
              followersL.append(profile.followers)
              followers_per_media.append(f_per_media)
              ratio.append(followers_following_ratio)
              ismicro.append(0)
              topics.append(hashtag)
              not_micro+=1
              
              interactions.append(inter1)
              urls.append(ur1)
              caption.append(captions1)
        
  
  user_data = pd.DataFrame(list(zip(users_id,username, followersL,followers_per_media,ratio,caption, urls, interactions,topics, ismicro)),
              columns=['id','username','followers','followers_per_media','followers_following_ratio', 'caption','urls', 'interactions','topic','micro'])
  
  return user_data


tags = [] #insert here the tags

d = scraper(tags,L)
print(d)
d.to_csv('usersInstagram.csv', encoding='UTF8',index=False)
print("Users dataset created")
