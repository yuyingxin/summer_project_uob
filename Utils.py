import datetime
import multiprocessing.dummy as mp
import os
from newsapi import NewsApiClient
from pyprocessing import textSize, fill, text
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 \
    import Features, EmotionOptions, EntitiesOptions
import urllib.request
from News import News
from PIL import Image
import json

global downloadPath
downloadPath = "downloads"

def labelDisplay(emotionCount):
    textSize(10)
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

    for i in range(0, len(response)):
        try:
            entityTextList.append(response[i]['entities'][0]['text'])
        except IndexError:
            entityTextList.append(None)
            print("Agent", i, "have no entity")

    # print(entityTextList)
    return entityTextList


def nluInit():
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        username='477799fe-c096-4cc4-be04-f8eca3658fc6',
        password='YLxDO8BkAOAc',
        version='2018-03-16'
    )
    return natural_language_understanding


def textAnalyse(url, natural_language_understanding):

    response = natural_language_understanding.analyze(
        url=url,
        features=Features(entities=EntitiesOptions(
            sentiment=False,
            emotion=False,
            limit=1
        ), emotion=EmotionOptions()
        )
    )

    return response


def downloader(url, index):
    global downloadPath
    # If download path is not existed, make a new one
    if not os.path.exists(downloadPath):
        os.mkdir(downloadPath)
    # Name the image files according to the index of them
    fileName = str(index).zfill(3) + '.PNG'
    # Generate the file path
    filePath = '{}{}{}'.format(downloadPath, os.sep, fileName)
    # If the file is already existed, delete it to avoid the history
    if os.path.exists(filePath):
        os.remove(filePath)

    opener = urllib.request.build_opener()
    opener.addheaders = [('User-Agent',
                          'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0')]
    urllib.request.install_opener(opener)
    try:
        urllib.request.urlretrieve(url=url, filename=filePath)
    except urllib.error.HTTPError:
        print("Agent", index, "have no image!")

    return filePath


def featureExtract(natural_language_understanding, articleNum, dateFrom, dateTo):
    """
    Extracting features from news (including retrieving news articles and analysing them by api)
    :param natural_language_understanding: credentials of IBM api
    :param articleNum: number of news articles that needs to be retrieved
    :param dateFrom: starting date of news
    :param dateTo: ending date of news
    :return: 1.emotional status of each article, 2.entities and 3.its relevance of each article,
    4.paths of saved images of each article, 5.titles of each articles
    """
    # Retrieve news (url, title and image) from google api
    newsList = getNews(articleNum, dateFrom, dateTo)

    # Download images and return saved path
    titles = []
    for i in range(0, articleNum):
        # paths.append(downloader(newsList[i].imageUrl, i))
        titles.append(newsList[i].title)
    t_download = datetime.datetime.now()  # Computing time cost on text analyse
    pool_download = mp.Pool(processes=articleNum)
    paths = [pool_download.apply(downloader, args=(newsList[i].imageUrl, i)) for i in range(0, articleNum)]
    print("Time cost on downloading images:" + str(datetime.datetime.now() - t_download))  # Print the time cost

    # Multiprocessing (for analysing article text - fail because of blocking by IBM api)
    pool = mp.Pool(processes=articleNum)

    t = datetime.datetime.now()  # Computing time cost on text analyse
    responses = [pool.apply(textAnalyse, args=(newsList[i].url, natural_language_understanding))
                 for i in range(0, articleNum)]
    print("Time cost on text analyse:" + str(datetime.datetime.now() - t))  # Print the time cost

    # Save json file on local
    global downloadPath
    if not os.path.exists(downloadPath):
        os.mkdir(downloadPath)
    fileName = "response_file.json"
    filePath = '{}{}{}'.format(downloadPath, os.sep, fileName)
    if os.path.exists(filePath):
        os.remove(filePath)

    f = open(filePath, "a")
    f.write(json.dumps(responses))
    f.close()

    strResponses = open(filePath, "r").read()
    responses = json.loads(strResponses)

    # emotionList: 2-d list, each list inside is an article and elements inside is the scores on each emotional type
    emotionList = parsingEmotion(responses)
    entityList = parsingEntities(responses)
    return emotionList, entityList, paths, titles


def offlineFeatureExtraction(articleNum):
    filePaths = []
    for i in range(0, articleNum):
        fileName = str(i).zfill(3) + '.PNG'
        filePath = '{}{}{}'.format(downloadPath, os.sep, fileName)
        filePaths.append(filePath)

    fileName = "response_file.json"
    filePath = '{}{}{}'.format(downloadPath, os.sep, fileName)
    strResponses = open(filePath, "r").read()
    responses = json.loads(strResponses)

    # emotionList: 2-d list, each list inside is an article and elements inside is the scores on each emotional type
    emotionList = parsingEmotion(responses)
    entityList = parsingEntities(responses)
    return emotionList, entityList, filePaths, titles


def paramExtract(emotionList):
    emotionIndex = []
    emotionCount = []
    emotionLevel = []  # EmotionLevel represents the weight of domain emotion

    for i in range(0, len(emotionList)):  # len(entityList) is actually the number of articles
        index = emotionList[i].index(max(emotionList[i]))  # Find the domain emotion in each article
        emotionIndex.append(index)
        level = max(emotionList[i]) / sum(emotionList[i])  # The weight of domain emotion
        emotionLevel.append(level)

    for i in range(0, 5):  # 5: the number of emotion
        emotionCount.append(emotionIndex.count(i))  # Count the number of articles on each emotion type

    return emotionIndex, emotionCount, emotionLevel


def compressImage(imagePaths):
    for path in imagePaths:
        if os.path.exists(path):
            img = Image.open(path)
            w, h = img.size
            if h > 120:
                w *= (120 / h)
                h = 120
            dImg = img.resize((int(w), h), Image.ANTIALIAS)
            dImg.save(path)

