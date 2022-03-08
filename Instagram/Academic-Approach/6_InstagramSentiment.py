import pandas as pd
from langdetect import detect
import numpy as np
import re
import stopwordsiso as stopwords
from emoji import demojize
from nltk.stem.wordnet import WordNetLemmatizer
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax


tokenizer = AutoTokenizer.from_pretrained("cardiffnlp/twitter-roberta-base-sentiment")

model = AutoModelForSequenceClassification.from_pretrained("cardiffnlp/twitter-roberta-base-sentiment")

model.save_pretrained("cardiffnlp/twitter-roberta-base-sentiment")

#nlp clean sentence based
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

df = pd.read_csv("usersInstagramMicroTopic.csv")
caption = df['caption']
pictures = df['picsText']

#lists to store new columns
all_caps=[]
all_pics=[]

positiveSentimentCap=[]
neutralSentimentCap=[]
negativeSentimentCap=[]
positiveSentimentPic=[]
neutralSentimentPic=[]
negativeSentimentPic=[]
labels = ['negative', 'neutral', 'positive']

for j in range(0,len(df['id'])):
    capList= []
    picList=[]
    posCap=[]
    neuCap=[]
    negCap=[]
    posPic=[]
    neuPic=[]
    negPic=[]
    #clean and sentiment analysis for both captions and picsTexts
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
    

#create final dataset
df['caption']= all_caps
df['picsText']= all_pics

df['positiveSentimentCaptions']= positiveSentimentCap
df['neutralSentimentCaptions']= neutralSentimentCap
df['negativeSentimentCaptions']= negativeSentimentCap

df['positiveSentimentPics']= positiveSentimentPic
df['neutralSentimentPics']= neutralSentimentPic
df['negativeSentimentPics']= negativeSentimentPic

df.to_csv('usersInstagramSentiment.csv', encoding='UTF8',index=False)
print("Sentiment dataset created")
