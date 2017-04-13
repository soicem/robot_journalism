from urllib.request import urlopen
from bs4 import BeautifulSoup
import datetime
import random
import re

import mysqlDB


class Article():
    def __init__(self, tendency, keyword):
        self.mq = mysqlDB.mysqlDB()

        self.keyword = keyword # specific keyword related to politic
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

        self.visitedUrl = []

        random.seed(datetime.datetime.now())


    def gathering(self):
        def getLinks(articleUrl, i):
            url = self.progressivismTargets[self.progressive[i]] + articleUrl
            html = urlopen(url)
            bsObj = BeautifulSoup(html, "html.parser")

            if i == 0: # 0 : 한겨례
                articleList = bsObj.findAll("div", {"class": "text"})
                titles = bsObj.findAll("span", {"class": "title"})
                published_times = bsObj.find_all('meta', attrs={'property':'article:published_time'})

                article_result = ""
                title = ""
                p_time = ""

                bool_title = 0

                for buf in titles:
                    title = buf.get_text()
                    bool_title = title.count(self.keyword) if True else False
                if bool_title:
                    for published_time in published_times:
                        re_date = re.compile(r'(\d{1,4}[/-]\d{1,2}[/-]\d{1,2}[T]\d{1,2}[/:]\d{1,2}[/:]\d{1,2}[+]\d{1,2}[/-:]\d{1,2})')
                        p_time = re_date.findall(str(published_time))

                    for name in articleList:  article_result += name.getText().strip().replace("\n", "").replace('"', "/")
                    if (title is not ""):
                        p_time = (p_time[0])[0:10] + " " + (p_time[0])[11:19]
                        self.mq.insert_data(str(1), title, "한겨례", article_result, url, p_time)

                return bsObj.find().findAll("a", href=re.compile("^(/arti/politics/)((?!:).)*$"))
            else:
                pass

        if self.tendency == "progressivism":
            links = getLinks(self.progressiveArticle[self.progressive[0]], 0)
            for i in range(50):
                newArticle = links[random.randint(0, len(links) - 1)].attrs["href"]
                if self.visitedUrl.count(newArticle) or newArticle.count("defense") > 0 :
                    continue
                self.visitedUrl.append(newArticle)
                print(self.visitedUrl)

                print(newArticle)
                links = getLinks(newArticle, 0)
            print(len(self.visitedUrl))
        elif self.status == "conservatism":
            pass





