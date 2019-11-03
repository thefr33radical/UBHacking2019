import json
import requests
from datetime import datetime
from urllib.parse import quote
from bs4 import BeautifulSoup

steps = 10
class News(object):
    def __init__(self):        
        self.key = "8ed21a03ae61438cafa2cccaee9cc967"

    def get_news(self, keyword):
        try:

            url = ('https://newsapi.org/v2/everything?'
                'q=%s&'
                'from=%s&'
                'sortBy=popularity&'
                'pageSize=5&'
                'apiKey=%s'
                % (keyword, datetime.today().strftime('%Y-%m-%d'), "8ed21a03ae61438cafa2cccaee9cc967"))

            response = requests.get(url)

            return response.json()
        except:
            return {"Title":"Error Fetching News"}

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
    pass
    """
    try:
        wiki = Wiki()
        
        wiki_results = wiki.get_wiki("apple")
        p=wiki_results["query"]["pages"]
        q=list(p.keys())
        print(p[q[0]]["extract"])
    except:
        print("error")
   """
    """
    try:

        news = News()
        news_results = news.get_news("apple")        
        return json.dumps({"desc":news_results["articles"][0]["title"]})   
    except:
        return json.dumps({"desc":"Wiki not found about"+dname})
        """
