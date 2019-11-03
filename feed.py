import json
import requests
from datetime import datetime

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

if __name__ == "__main__":
    # Initialize the news object
    news = News()

    # Grab some news
    results = news.get_news("apple")
    print(results)