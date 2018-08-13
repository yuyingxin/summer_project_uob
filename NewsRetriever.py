from newsapi import NewsApiClient


class NewsRetriever:
    def __init__(self, articleNum, dateFrom, dateTo):
        self.articleNum = articleNum
        self.dateFrom = dateFrom
        self.dateTo = dateTo

    def getUrls(self):
        url_articles = []
        # Extracting news articles from google news api
        # Setting up request and requesting (google news api)
        newsApi = NewsApiClient(api_key='75c1a72801204ed9ae67fa55057ea869')
        articles = newsApi.get_everything(sources='bbc-news',  # limit search by source index (in documentation)
                                          from_param=self.dateFrom,
                                          to=self.dateTo,
                                          language='en',
                                          sort_by='popularity',
                                          page_size=self.articleNum,
                                          page=1)

        # Parsing url of each article from response
        for i in range(0, len(articles['articles'])):
            url_articles.append(articles['articles'][i]['url'])

        return url_articles
