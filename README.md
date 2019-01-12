# Sentiment-Analysis
Sentiment Analysis on Twitter Tweets using NLP library TextBlob.

# The Approach
The tasks performed in this project are as following:
```
◆ Stream twitter tweets into MongoDB
◆ Analyze the tweets saved in mongoDb
◆ Save the result into a csv file
```

# Development Guide
Install MongoDb : https://www.mongodb.com/download-center </br>
( incoming tweets are stored in mongodb as part of the requirement )</br>

All the python dependencies can be installed using pip. Just use the following command from the root directory of the project. </br>

1. Install the requirements. pip install -r requirements.txt</br>
2. Add your ACCESS_TOKEN, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET inside twitterKeys.py file.</br>
3. Run the code by executing the file tweets.py</br>
4. The tweets with currresponding result will be stored on out.csv file</br>
