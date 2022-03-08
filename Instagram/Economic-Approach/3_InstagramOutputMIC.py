import pandas as pd
from langdetect import detect
import numpy as np
import re
import stopwordsiso as stopwords
from emoji import demojize
from nltk.stem.wordnet import WordNetLemmatizer
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax
import pickle

#get models

Pkl1_Filename = "./Pickle_XGB_Model_Instagram.pkl"  
with open(Pkl1_Filename, 'rb') as file: 
    Pickled_XGB_Model = pickle.load(file)
    

Pkl2_Filename = "./Pickle_XGB_ModelMicroTopicInstagram.pkl"  
with open(Pkl2_Filename, 'rb') as file:  
    Pickled_XGB_ModelMicroTopic = pickle.load(file)
    


tokenizer = AutoTokenizer.from_pretrained("cardiffnlp/twitter-roberta-base-sentiment")

model = AutoModelForSequenceClassification.from_pretrained("cardiffnlp/twitter-roberta-base-sentiment")

model.save_pretrained("cardiffnlp/twitter-roberta-base-sentiment")


#obtain most common language
def most_common(lst):
    return max(set(lst), key=lst.count)

#nlp clean text sentence based
def clean_text(text):
    try:
        language = detect(text)
    except:
        language = "Not available"

    if(stopwords.has_lang(language)):
      stop = stopwords.stopwords(language)
    else:
      stop = stopwords.stopwords("en")

    text = demojize(text) #convert emojis to text
    temp = text.lower()
    temp = re.sub("'", "", temp) # to avoid removing contractions in english
    temp = re.sub("@[A-Za-z0-9_]+","", temp) #remove entire tag (@ and also name tagged)
    temp = re.sub("#","", temp) #remove only hashtag symbol
    temp = re.sub(r'http\S+', '', temp)  #remove links
    temp = re.sub('[()!?.,;:]', ' ', temp) #remove ()!?.,:;
    temp = re.sub('\[.*\].*',' ', temp) #remove []
    temp = re.sub("[^a-z]"," ", temp) #remove numbers
    temp = temp.split()
    temp = [w for w in temp if not w in stop] #remove stopwords
    temp = [WordNetLemmatizer().lemmatize(w, pos='v') for w in temp] #not for sentence based
    temp = " ".join(word for word in temp)
    return temp

#read csv
df = pd.read_csv("InputInstagramPics.csv")
caption = df['captions']
pictures = df['picsText']
users = df['username']
topic = df['topic']

#lists to store values
all_caps=[]
all_pics=[]
positiveSentimentCap=[]
neutralSentimentCap=[]
negativeSentimentCap=[]
positiveSentimentPic=[]
neutralSentimentPic=[]
negativeSentimentPic=[]
topicPercentageInCaptions = []
wordsPercentageInCaptions = []
topicPercentageInPics = []
wordsPercentageInPics = []
userLanguage=[]
#labels for sentiiment analysis
labels = ['negative', 'neutral', 'positive']


#topic research inside captions
for i in range(0,len(df['id'])):
    #counters
    cap=0 #captions
    f=0 #topics found
    wo=0 #words
    langs=[]
    #for each caption
    for ca in caption[i].split("', "):
        for c in ca.split('", '):
            #flag to avoid multiple topics written in the same caption
            found = False 
            #increase number of captions
            cap+=1
            
            #evaluate tweet language (subset)
            if (cap%5==0):
                try:
                    language = detect(c)
                except:
                    language = "Not available"
                
                langs.append(language)
                
            
            #for each word
            for w in c.split(" "):
                    #count how many times the topic is written
                if (topic[i].lower() in w.lower() and found==False):
                    f+=1
                    found=True
                #increase number of words
                wo+=1
    #evaluate how many times the topic is written inside captions
    print(f, "topic word over",cap, "captions with", wo, "total words")
    percT = ((f)/cap)*100
    #evaluate percentage of word topic written with respect to all words
    percW = ((f)/wo)*100
    print("Percentage of topic", topic[i]," in captions = ", percT, "%")
    print("Percentage of topic", topic[i]," in words = ", percW, "%")
    #evaluate most common language for the user
    finalLanguage = most_common(langs)
    print(finalLanguage)
    print("\n")

    topicPercentageInCaptions.append(percT)
    wordsPercentageInCaptions.append(percW)
    userLanguage.append(finalLanguage)

#topic research inside picsText
for i in range(0,len(df['id'])):
    #counters
    pics=0 #pics
    f=0 #topics found
    wo=0 #words
    #for each pic
    for ca in pictures[i].split("', "):
        for c in ca.split('", '):
            #flag to avoid multiple topics written in the same pic
            found = False 
            #increase number of captions
            pics+=1
            #for each word
            for w in c.split(" "):
                    #count how many times the topic is written
                if (topic[i].lower() in w.lower() and found==False):
                    f+=1
                    found=True
                #increase number of words
                wo+=1
    #evaluate how many times the topic is written inside pics
    print(f, "topic word over",pics, "pics with", wo, "total words")
    percT = ((f)/pics)*100
    #evaluate percentage of word topic written with respect to all words
    percW = ((f)/wo)*100
    
    print("Percentage of topic", topic[i]," in pics = ", percT, "%")
    print("Percentage of topic", topic[i]," in words = ", percW, "%")


    topicPercentageInPics.append(percT)
    wordsPercentageInPics.append(percW)

#add new columns to the dataset
df['topicInCaptionsPercentage']= topicPercentageInCaptions
df['topicInWordsPercentage']= wordsPercentageInCaptions
df['topicInPicsPercentage']= topicPercentageInPics
df['topicInPicsWordsPercentage']= wordsPercentageInPics
df['language']= userLanguage




#sentiment analysis for both captions and picsTexts
for j in range(0,len(df['id'])):
    capList= []
    picList=[]
    posCap=[]
    neuCap=[]
    negCap=[]
    posPic=[]
    neuPic=[]
    negPic=[]
    for cap in caption[j].split("', "):
      #another split to handle "
      for c in cap.split('", '):
        t = clean_text(c)
        capList.append(t)
        if(len(t)>300):
            t=t[0:300]
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
                posCap.append(s)
            elif(l=='neutral'):
                neuCap.append(s)
            else:
                negCap.append(s)
    all_caps.append(capList)
    positiveSentimentCap.append(np.mean(posCap))
    neutralSentimentCap.append(np.mean(neuCap))
    negativeSentimentCap.append(np.mean(negCap))

    for pic in pictures[j].split("', "):
      #another split because replies use " instead of '
      for p in pic.split('", '):
        t2 = clean_text(p)
        picList.append(t2)
        if(len(t2)>300):
            t2=t2[0:300]
        encoded_input2 = tokenizer(t2, return_tensors='pt')
        output2 = model(**encoded_input2)
        scores2 = output2[0][0].detach().numpy()
        scores2 = softmax(scores2)

        ranking2 = np.argsort(scores2)
        ranking2 = ranking2[::-1]
        for i in range(scores2.shape[0]):
            l2 = labels[ranking2[i]]
            s2 = scores[ranking2[i]]
            if(l2=='positive'):
                posPic.append(s2)
            elif(l2=='neutral'):
                neuPic.append(s2)
            else:
                negPic.append(s2)
    all_pics.append(picList)
    positiveSentimentPic.append(np.mean(posPic))
    neutralSentimentPic.append(np.mean(neuPic))
    negativeSentimentPic.append(np.mean(negPic))
    
#add new columns
df['captions']= all_caps
df['picsText']= all_pics

df['positiveSentimentCaptions']= positiveSentimentCap
df['neutralSentimentCaptions']= neutralSentimentCap
df['negativeSentimentCaptions']= negativeSentimentCap

df['positiveSentimentPics']= positiveSentimentPic
df['neutralSentimentPics']= neutralSentimentPic
df['negativeSentimentPics']= negativeSentimentPic


#select X 
X = df.loc[:, ["followers", "followers_per_media","followers_following_ratio","interactions","topicInCaptionsPercentage", "topicInWordsPercentage", "topicInPicsPercentage","topicInPicsWordsPercentage",
"positiveSentimentCaptions","neutralSentimentCaptions" ,"negativeSentimentCaptions","positiveSentimentPics","neutralSentimentPics" ,"negativeSentimentPics"]]
X = X.to_numpy()

#predict
Ypredict = Pickled_XGB_Model.predict(X)

YpredictMicroTopic = Pickled_XGB_ModelMicroTopic.predict(X) 

#for each user print as output the results for both Micro Influencer and Micro Topic Influencer
for i in range(len(users)):
    if(Ypredict[i]==1):
        print(users[i],"is a microinfluencer")
    else:
        print(users[i],"is NOT a microinfluencer")
    
    if(YpredictMicroTopic[i]==1):
        print(users[i],"is a microinfluencer for the topic", topic[i])
    else:
        print(users[i],"is NOT a microinfluencer for the topic", topic[i])
