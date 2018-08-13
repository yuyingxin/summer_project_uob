import datetime
import multiprocessing.dummy as mp
import os
from newsapi import NewsApiClient
from pyprocessing import textSize, fill, text
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 \
    import Features, EntitiesOptions, EmotionOptions
import urllib.request
from News import News
from PIL import Image


def labelDisplay(emotionCount):
    textSize(12)
    fill(120, 225, 255)
    text("Sadness: {0}".format(emotionCount[0]), 5, 15)
    fill(255, 167, 0)
    text("Joy: {0}".format(emotionCount[1]), 5, 30)
    fill(0, 0, 0)
    text("Fear: {0}".format(emotionCount[2]), 5, 45)
    fill(141, 85, 36)
    text("Disgust: {0}".format(emotionCount[3]), 5, 60)
    fill(214, 45, 32)
    text("Anger: {0}".format(emotionCount[4]), 5, 75)


def getNews(articleNum, dateFrom, dateTo):
    # url_articles = []
    # title_articles = []
    # image_articles = []
    newsList = []

    # Extracting news articles from google news api
    # Setting up request and requesting (google news api)
    newsApi = NewsApiClient(api_key='75c1a72801204ed9ae67fa55057ea869')
    articles = newsApi.get_everything(sources='bbc-news',  # limit search by source index (in documentation)
                                      from_param=dateFrom,
                                      to=dateTo,
                                      language='en',
                                      sort_by='popularity',
                                      page_size=articleNum,
                                      page=1)

    # Parsing url of each article from response
    for i in range(0, len(articles['articles'])):
        news = News(articles['articles'][i]['title'], articles['articles'][i]['url'], articles['articles'][i]['urlToImage'])
        # url_articles.append(articles['articles'][i]['url'])
        # title_articles.append(articles['articles'][i]['title'])
        # image_articles.append(articles['articles'][i]['urlToImage'])
        newsList.append(news)

    # return url_articles, title_articles, image_articles
    return newsList


def parsingEmotion(response):
    emotionList = []
    # Parsing response from IBM
    # Emotion
    for i in range(0, len(response)):
        emotion = [float(response[i]['emotion']['document']['emotion']['sadness']),
                   float(response[i]['emotion']['document']['emotion']['joy']),
                   float(response[i]['emotion']['document']['emotion']['fear']),
                   float(response[i]['emotion']['document']['emotion']['disgust']),
                   float(response[i]['emotion']['document']['emotion']['anger'])]
        # emotion.index(max(emotion)) # return the max score of emotion
        emotionList.append(emotion)
    # print(emotionList)
    return emotionList


def parsingEntities(response):
    entityTextList = []
    entityRelevanceList = []

    for i in range(0, len(response)):
        entityText = []
        entityRelevance = []
        for j in range(0, len(response[i]['entities'])):
            entityText.append(response[i]['entities'][j]['text'])
            entityRelevance.append(float(response[i]['entities'][j]['relevance']))
        entityTextList.append(entityText)
        entityRelevanceList.append(entityRelevance)

    # print(entityTextList)
    return entityTextList, entityRelevanceList


def nluInit():
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        username='477799fe-c096-4cc4-be04-f8eca3658fc6',
        password='YLxDO8BkAOAc',
        version='2018-03-16'
    )
    return natural_language_understanding


def textAnalyse(url, entityNum, natural_language_understanding):
    # responseList = []
    # Text processing by IBM api via url
    # Set up request (IBM api)

    # Requesting
    # for i in range(0, len(urls)):
    #     response = natural_language_understanding.analyze(
    #         url=urls[i],
    #         features=Features(entities=EntitiesOptions(
    #             sentiment=False,
    #             emotion=False,
    #             limit=entityNum
    #         ), emotion=EmotionOptions()
    #                           )
    #     )
    #     responseList.append(response)

    response = natural_language_understanding.analyze(
        url=url,
        features=Features(entities=EntitiesOptions(
            sentiment=False,
            emotion=False,
            limit=entityNum
        ), emotion=EmotionOptions()
        )
    )

    return response


def downloader(url, index):
    fileName = str(index).zfill(3) + '.jpg'
    path = '{}{}{}'.format('downloads', os.sep, fileName)
    urllib.request.urlretrieve(url, path)
    return path


def featureExtract(natural_language_understanding, articleNum, entityNum, dateFrom, dateTo):
    """
    Extracting features from news (including retrieving news articles and analysing them by api)
    :param natural_language_understanding: credentials of IBM api
    :param articleNum: number of news articles that needs to be retrieved
    :param entityNum: number of entities in each article that needs to be extracted
    :param dateFrom: starting date of news
    :param dateTo: ending date of news
    :return: 1.emotional status of each article, 2.entities and 3.its relevance of each article,
    4.paths of saved images of each article, 5.titles of each articles
    """
    # Retrieve news (url, title and image) from google api
    newsList = getNews(articleNum, dateFrom, dateTo)

    # Download images and return saved path
    paths = []
    titles = []
    for i in range(0, articleNum):
        paths.append(downloader(newsList[i].imageUrl, i))
        titles.append(newsList[i].title)

    # Multiprocessing (for analysing article text - fail because of blocking by IBM api)
    pool = mp.Pool(processes=articleNum)

    t = datetime.datetime.now()  # Computing time cost on text analyse
    responses = [pool.apply(textAnalyse, args=(newsList[i].url, entityNum, natural_language_understanding))
                 for i in range(0, articleNum)]
    print("Time cost on text analyse:" + str(datetime.datetime.now() - t))  # Print the time cost

    emotionList = parsingEmotion(responses)
    textList, relevanceList = parsingEntities(responses)
    return emotionList, textList, relevanceList, paths, titles


def paramExtract(entityList, emotionList):
    groupSizes = []
    emotionIndex = []
    emotionCount = []

    for i in range(0, len(entityList)):
        groupSizes.append(len(entityList[i]))  # How many entities in each article (group)
        emotionIndex.append(emotionList[i].index(max(emotionList[i])))  # Find the domain emotion in each article

    for i in range(0, 5):  # 5: the number of emotion
        emotionCount.append(emotionIndex.count(i))

    return groupSizes, emotionIndex, emotionCount


def compressImage(imagePaths):
    wList = []
    hList = []
    for path in imagePaths:
        img = Image.open(path)
        w, h = img.size
        if w > 200:
            h *= (200 / w)
            w = 200
        wList.append(w)
        hList.append(int(h))
        dImg = img.resize((w, int(h)), Image.ANTIALIAS)
        dImg.save(path)
    return wList, hList

