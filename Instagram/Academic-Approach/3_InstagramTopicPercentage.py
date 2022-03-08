import csv
import pandas as pd
import langdetect
from langdetect import detect



#obtain most common language
def most_common(lst):
    return max(set(lst), key=lst.count)


df = pd.read_csv("usersInstagramPics.csv")

captions = df['caption']
picsText = df['picsText']
ids = df['id']
topic = df['topic']

#lists to store new columns
topicPercentageInCaptions = []
wordsPercentageInCaptions = []
topicPercentageInPics = []
wordsPercentageInPics = []
userLanguage=[]

for i in range(0,len(ids)):
    #counters
    cap=0 #captions
    f=0 #topics found
    wo=0 #words
    langs=[]
    #for each caption
    for ca in captions[i].split("', "):
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


for i in range(0,len(ids)):
    #counters
    pics=0 #pics
    f=0 #topics found
    wo=0 #words
    #for each pic
    for ca in picsText[i].split("', "):
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
    print(f, "topic word over",pics, "captions with", wo, "total words")
    percT = ((f)/pics)*100
    #evaluate percentage of word topic written with respect to all words
    percW = ((f)/wo)*100
    print("Percentage of topic", topic[i]," in pics = ", percT, "%")
    print("Percentage of topic", topic[i]," in words = ", percW, "%")
    print("\n")

    topicPercentageInPics.append(percT)
    wordsPercentageInPics.append(percW)
    


df['topicInCaptionsPercentage']= topicPercentageInCaptions
df['topicInWordsPercentage']= wordsPercentageInCaptions
df['topicInPicsPercentage']= topicPercentageInPics
df['topicInPicsWordsPercentage']= wordsPercentageInPics
df['language']= userLanguage


print(df.head())
print(df.info())
df.to_csv('usersInstagramPercentages.csv', encoding='UTF8',index=False)

print("Percentages dataset created")
