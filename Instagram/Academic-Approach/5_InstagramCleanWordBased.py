import pandas as pd
import nltk
#nltk.download('wordnet')
from langdetect import detect
import numpy as np
import re
import stopwordsiso as stopwords
import emoji
from emoji import demojize
from nltk.stem.wordnet import WordNetLemmatizer

df = pd.read_csv("usersInstagramMicroTopic.csv")

#nlp clean text word based
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
    return temp


caption = df['caption']
pictures = df['picsText']
all_caps=[]
all_pics=[]
for j in range(0,len(df['id'])):
  capList= []
  for cap in caption[j].split("', "):
      #another split to handle "
      for c in cap.split('", '):
        t = clean_text(c)
        
        for k in t:
          capList.append(k)
  all_caps.append(capList)
  picList= []
  for pic in pictures[j].split("', "):
      #another split because replies use " instead of '
      for p in pic.split('", '):
        t2 = clean_text(p)
        
        for k2 in t2:
          picList.append(k2)
  all_pics.append(picList)


df['caption']= all_caps
df['picsText'] = all_pics
df.to_csv('usersInstagramCleanWordBased.csv', encoding='UTF8',index=False)
print("Clean Word Based dataset created")
