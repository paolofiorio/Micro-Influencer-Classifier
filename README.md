# Micro-Influencer-Classifier
Repository of my master's degree thesis in Data Science and Engineering at "Politecnico di Torino"

### Two Social networks implementations
* Twitter
* Instagram

### Two approaches:
* Academic approach
* Economic approach

# TWITTER SECTION
## Academic Approach

### 1_TwitterUsersRetrieval.py 

This first script requires:
* a valid Twitter developer account 
* the insertion of its consumer_key and consumer_secret inside the code
* the insertion of language and topics of interest (considering the high quantity of topics to work with, it is asked to write them directly inside code and not through command line for an easier use)

With the inserted topics the script for each of them will retrieve 5 micro influencers and 5 not micro influencers with all their metrics and will insert them in a proper csv file.

### 2_TwitterTweetsRetrieval.py

This second script requires:
* a valid Twitter developer account 
* the insertion of its consumer_key and consumer_secret inside the code

The previous csv file will be enriched with 200 tweets (no retweets) for each user.

### 3_TwitterTopicPercentages.py 

The third script individuates the language of each user and analyses the presence of the topic word inside tweets and words providing two new metrics.
The previous csv file is enriched with these new metrics for each user.

### 4_TwitterRanking.py 

With al the obtained metrics a ranking is created, based on their distributions, to establish if each user can be considered as topic micro influencer or not.
The previous csv file is enriched with the score established in this script.


### 5_TwitterCleanWordBased.py 

Additional script in case a word based study is requested.


### 6_TwitterSentiment.py

Script that provides a text preprocessing phase and a sentiment analysis for each user.

Three new metrics are added inside the dataset:
* Positive sentiment score
* Neutral sentiment score
* Negative sentiment score

These 3 new metrics are added to csv file with a new column "MicroTopic" that assigns 1 to each user having the 4th script score > of the scores' mean, 0 otherwise.

### 7_TwitterModelSelection.ipynb

The last step is provided on Google Colab (GPU requested), it requires to clone the proper github repository or import sentiment csv file.

This script searches for both micro influencer classification and micro topic influencer classification the best model between:
* Random Forest
* XGBoost
* SVC
* MLP
* LOGISTIC REGRESSION
* SGD


## Economic Approach

### TwitterMIC.py 

This script requires:
* a valid Twitter developer account 
* the insertion of its consumer_key and consumer_secret inside the code
* the import of the best models obtained from academic approach for both micro influencer classification and micro topic influencer classification
* the insertion from command line of the list of users that the brand wants to analyze and the insertion of the specific topic


For each user all the metrics are evaluated by the script to provide as final output the classification results:
* is the inserted user a micro influencer? Y/N
* is the inserted user a micro influencer of the specific topic? Y/N



# INSTAGRAM SECTION
## Academic Approach

### 1_InstagramUsersRetrieval.py 

This first script requires:
* a valid Instagram account
* the insertion of its username and password inside the code
* the insertion of the list topics of interest (considering the high quantity of topics to work with, it is asked to write them directly inside code and not through command line for an easier use)

With the inserted topics the script will retrieve for each of them 5 micro influencers and 5 not micro influencers with all their metrics and image urls and will insert them in a proper csv file.

### 2_InstagramImageCaptioning.ipynb

This step is provided on Google Colab (GPU requested), it requires to clone the proper github repository or import sentiment csv files
To perform this script and obtain all models and datasets an authorization with GoogleCredentials is asked.

The user can select between two different datasets: 
* COCO 
* Conceptual captions

For each user the 25 image previously obtained are selected by the script and converted to textual caption.
The previous csv file will be enriched with a column providing the image captions obtained.

### 3_InstagramTopicPercentage.py 

The third script individuates the language of each user and analyses the presence of the topic word inside posts descriptions, captions and their respective words providing four new metrics.
The previous csv file is enriched with these new metrics for each user.

### 4_InstagramRanking.py 

With al the obtained metrics a ranking is created, based on their distributions, to establish if each user can be considered as topic micro influencer or not. A new column "MicroTopic" that assigns 1 to each user having the score > of the scores' mean, 0 otherwise is added to the dataset.

The previous csv file is enriched with the score and the "MicroTopic" column established in this script.


### 5_InstagramCleanWordBased.py 

Additional script in case a word based study is requested.


### 6_InstagramSentiment.py

Script that provides a text preprocessing phase and a sentiment analysis for each user.

Six new metrics(for posts decriptions and captions obtained from step 2) are added inside the dataset :
* Positive sentiment scores
* Neutral sentiment scores
* Negative sentiment scores

These 6 new metrics are added to csv file.

### 7_InstagramModelSelection.ipynb

The last step is provided on Google Colab (GPU requested), it requires to clone the proper github repository or import sentiment csv files.

This script searches for both micro influencer classification and micro topic influencer classification the best model between:
* Random Forest
* XGBoost
* SVC
* MLP
* LOGISTIC REGRESSION
* SGD


## Economic Approach

### 1_InstagramInputMIC.py 

This script requires:
* a valid Instagram account
* the insertion of its username and password inside the code
* the insertion from command line of the list of users that the brand wants to analyze and the insertion of the specific topic


This script works as the 1_InstagramUsersRetrieval.py but only for the inserted list of users. 




### 2_InstagramImageCaptioningEconomic.ipynb

This step is provided on Google Colab (GPU requested), it requires to clone the proper github repository or import sentiment csv file.
To perform this script and obtain all models and datasets an authorization with GoogleCredentials is asked.

The user can select between two different datasets: 
* COCO 
* Conceptual captions

For each user the 25 image previously obtained are selected by the script and converted to textual caption.
The previous csv file will be enriched with a column providing the image captions obtained.


### 3_InstagramOutputMIC.py 

This script requires:
* a valid Instagram account
* the insertion of its username and password inside the code
* the import of the best models obtained from academic approach for both micro influencer classification and micro topic influencer classification


Once obtained basic metrics and textual captions, for each user all the metrics are evaluated by the script to provide as final output the classification results:
* is the inserted user a micro influencer? Y/N
* is the inserted user a micro influencer of the specific topic? Y/N
