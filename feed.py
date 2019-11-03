import json
import requests
from datetime import datetime
from urllib.parse import quote

steps = 10
class News(object):
    def __init__(self):
        with open("./global.config") as f:
            self.config = json.load(f)
        self.key = self.config["news_api_key"]

    def get_news(self, keyword):
        url = ('https://newsapi.org/v2/everything?'
               'q=%s&'
               'from=%s&'
               'sortBy=popularity&'
               'pageSize=5&'
               'apiKey=%s'
               % (keyword, datetime.today().strftime('%Y-%m-%d'), self.key))

        response = requests.get(url)

        return response.json()

class Wiki(object):
    def __init__(self):
        pass

    def get_wiki(self, keyword):
        url = ('https://en.wikipedia.org/w/api.php?'
               'action=query&'
               'prop=extracts&'
               'format=json&'
               'exintro=&'
               'titles=%s'
               % (quote(keyword)))  # encode the URL

        response = requests.get(url)

        return response.json()

if __name__ == "__main__":
    # Initialize the feed objects
    news = News()
    wiki = Wiki()

    # Grab some feeds
    news_results = news.get_news("apple")
    print(news_results)
    wiki_results = wiki.get_wiki("nasdaq")
    print(wiki_results)