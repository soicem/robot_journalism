from urllib.request import urlopen
from bs4 import BeautifulSoup
import datetime
import random
import re

class Article():
    def __init__(self, status):
        self.status = status
        self.progressive = ["한겨례", "경향신문", "오마이뉴스"]
        self.progressivismTargets = {
            self.progressive[0]: "http://www.hani.co.kr/",
            self.progressive[1]: "http://www.khan.co.kr/",
            self.progressive[2]: "http://www.ohmynews.com/"}
        self.progressiveArticle = {
            self.progressive[0]: "/arti/politics/",
            self.progressive[1]: "",
            self.progressive[2]: ""
        }
        self.conservative = []
        self.conservatismTargets = {}

        random.seed(datetime.datetime.now())


    def gathering(self):
        def getLinks(articleUrl, i):
            html = urlopen(self.progressivismTargets[self.progressive[i]] + articleUrl)
            bsObj = BeautifulSoup(html, "html.parser")

            if i == 0:
                nameList = bsObj.findAll("div", {"class": "text"})
                for name in nameList:
                    print(name.get_text())
                return bsObj.find().findAll("a", href=re.compile("^(/arti/politics/)((?!:).)*$"))
            else:
                pass

        if self.status == "progressivism":
            links = getLinks(self.progressiveArticle[self.progressive[0]], 0)
            while len(links) > 0:
                newArticle = links[random.randint(0, len(links) - 1)].attrs["href"]
                print(newArticle)
                links = getLinks(newArticle, 0)
        elif self.status == "conservatism":
            pass



