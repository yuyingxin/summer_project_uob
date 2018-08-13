from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 \
    import Features, EntitiesOptions, KeywordsOptions, EmotionOptions, SentimentOptions
from newsapi import NewsApiClient

url_articles = []
responseList = []
entityText = []
emotionList = []
entityTextList = []
groupSizes = []

# Extracting news articles from google news api
# Setting up request and requesting (google news api)
news_api = NewsApiClient(api_key='75c1a72801204ed9ae67fa55057ea869')
all_articles = news_api.get_everything(sources='bbc-news',  # limit search by source index (in documentation)
                                       from_param='2018-07-31',
                                       to='2018-08-01',
                                       language='en',
                                       sort_by='popularity',
                                       page_size=5,
                                       page=1)

# Parsing url of each article from response
for i in range(0, len(all_articles['articles'])):
    url_articles.append(all_articles['articles'][i]['url'])

# Text processing by IBM api via url
# Set up request (IBM api)
natural_language_understanding = NaturalLanguageUnderstandingV1(
    username='477799fe-c096-4cc4-be04-f8eca3658fc6',
    password='YLxDO8BkAOAc',
    version='2018-03-16'
)

# Requesting
for i in range(0, len(url_articles)):
    response = natural_language_understanding.analyze(
        url=url_articles[i],
        features=Features(entities=EntitiesOptions(
            sentiment=False,
            emotion=False,
            limit=10
        ), emotion=EmotionOptions()
                          )
    )
    responseList.append(response)

# print(responseList)

# Parsing response from IBM
# Emotion
for i in range(0, len(responseList)):
    emotion = [float(responseList[i]['emotion']['document']['emotion']['sadness']),
               float(responseList[i]['emotion']['document']['emotion']['joy']),
               float(responseList[i]['emotion']['document']['emotion']['fear']),
               float(responseList[i]['emotion']['document']['emotion']['disgust']),
               float(responseList[i]['emotion']['document']['emotion']['anger'])]
    # emotion.index(max(emotion)) # return the max score of emotion
    emotionList.append(emotion)
print(emotionList)

# Entities
for i in range(0, len(responseList)):
    entityText = []
    for j in range(0, len(responseList[i]['entities'])):
        entityText.append(responseList[i]['entities'][j]['text'])
    entityTextList.append(entityText)

print(entityTextList)

for i in range(0, len(entityTextList)):
    groupSizes.append(len(entityTextList[i]))

print(groupSizes)

