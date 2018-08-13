import json
from google_images_download import google_images_download
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 \
    import Features, EntitiesOptions, KeywordsOptions, EmotionOptions, SentimentOptions
from newsapi import NewsApiClient

url_articles = []
responseList = []

# Extracting news articles from google news api
news_api = NewsApiClient(api_key='75c1a72801204ed9ae67fa55057ea869')
all_articles = news_api.get_everything(sources='bbc-news',
                                       from_param='2018-07-31',
                                       to='2018-08-01',
                                       language='en',
                                       sort_by='popularity',
                                       page_size=10,
                                       page=1)

for i in range(0, len(all_articles['articles'])):
    url_articles.append(all_articles['articles'][i]['url'])

# analyse text by IBM api
natural_language_understanding = NaturalLanguageUnderstandingV1(
    username='477799fe-c096-4cc4-be04-f8eca3658fc6',
    password='YLxDO8BkAOAc',
    version='2018-03-16'
)

for i in range(0, len(url_articles)):
    response = natural_language_understanding.analyze(
        url=url_articles[i],
        features=Features(entities=EntitiesOptions(
            sentiment=True,
            emotion=True,
            limit=30
        ), emotion=EmotionOptions()
                          ),
        clean=False
    )
    responseList.append(response)

print(responseList)
# print(json.dumps(response, indent=2))

# parsing response from IBM
entitiesText = []
emotionDoc = [float(response['emotion']['document']['emotion']['sadness']),
              float(response['emotion']['document']['emotion']['joy']),
              float(response['emotion']['document']['emotion']['fear']),
              float(response['emotion']['document']['emotion']['disgust']),
              float(response['emotion']['document']['emotion']['anger'])]
print(emotionDoc)
indexDoc = emotionDoc.index(max(emotionDoc))


for i in range(0, len(response['entities'])):
    if 'Guardian' in response['entities'][i]['text'] or 'Location' in response['entities'][i]['type']:
        pass
    else:
        entitiesText.append(response['entities'][i]['text'])
        print(response['entities'][i]['text'], response['entities'][i]['emotion']['sadness'],
              response['entities'][i]['emotion']['joy'], response['entities'][i]['emotion']['fear'],
              response['entities'][i]['emotion']['disgust'], response['entities'][i]['emotion']['anger'])

# response['entities'][i]['sentiment']['score'], response['entities'][i]['sentiment']['label'],



# sadness: color: grey (black, white) -less leaves
# joy: color: orange (yellow, green) -more leaves
# anger: color: red -more leaves
# disgust: no leaves
# fear: background: black
# the numbers of leaves represents the degree of emotion

# # request images based on keywords
# keywords = "{0},{1},{2}".format(entitiesText[0], entitiesText[1], entitiesText[2])
# resImg = google_images_download.googleimagesdownload()
# paths = resImg.download({"keywords": keywords, "limit": 5, "print_urls": True})
# print(paths)

# generator(indexDoc)