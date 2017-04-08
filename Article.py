from urllib.request import urlopen
from bs4 import BeautifulSoup
import datetime
import random
import re

import mysqlDB


class Article():
    def __init__(self, tendency):
        self.mq = mysqlDB.mysqlDB()
        self.tendency = tendency
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
            url = self.progressivismTargets[self.progressive[i]] + articleUrl
            html = urlopen(url)
            bsObj = BeautifulSoup(html, "html.parser")

            if i == 0: # 0 : 한겨례
                nameList = bsObj.findAll("div", {"class": "text"})
                titles = bsObj.findAll("span", {"class": "title"})
                published_times = bsObj.find_all('meta', attrs={'property':'article:published_time'})
                article_result = ""
                title = ""
                for buf in titles:
                    # print(title.get_text())
                    title = buf.get_text()
                p_time = ""
                for published_time in published_times:
                    p_date = re.compile(r'(\d{1,4}[/-]\d{1,2}[/-]\d{1,2}[T]\d{1,2}[/:]\d{1,2}[/:]\d{1,2}[+]\d{1,2}[/-:]\d{1,2})')
                    p_time = p_date.findall(str(published_time))

                for name in nameList:  article_result += name.getText().strip().replace("\n", "")
                if (title is not ""):
                    p_time = (p_time[0])[0:10] + " " + (p_time[0])[11:19]
                    self.mq.insert_data(str(1), title, "한겨례", article_result, url, p_time)

                return bsObj.find().findAll("a", href=re.compile("^(/arti/politics/)((?!:).)*$"))
            else:
                pass

        if self.tendency == "progressivism":
            links = getLinks(self.progressiveArticle[self.progressive[0]], 0)
            for i in range(10):
                newArticle = links[random.randint(0, len(links) - 1)].attrs["href"]
                print(newArticle)
                links = getLinks(newArticle, 0)
        elif self.status == "conservatism":
            pass





