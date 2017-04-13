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
            self.progressive[1]: "http://news.khan.co.kr/",
            self.progressive[2]: "http://www.ohmynews.com/"}
        self.progressiveArticle = {
            self.progressive[0]: "/arti/politics/",
            self.progressive[1]: "/kh_politics/",
            self.progressive[2]: "/NWS_Web/ArticlePage/Total_Article.aspx?PAGE_CD=C0400"
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


            elif i == 1:  # 경향신문
                nameList = bsObj.findAll("p", {"class": "content_text"})
                titles = bsObj.findAll("h1", {"id": "article_title"})
                published_time = bsObj.find('em').get_text()
                article_result = ""
                title = ""

                for buf in titles:
                    title = buf.get_text()
                print("title",title)

                p_time = published_time[5:]

                for name in nameList:  article_result += name.getText().strip().replace("\n", "")

                if (title is not ""):
                    self.mq.insert_data(str(1), title, "경향신문", article_result, url, p_time)

                return bsObj.find().findAll("a", href=re.compile("khan_art_view.html[/?]artid=2017"))

            elif i == 2:  # 오마이뉴스
                print("url =", url)
                nameList = bsObj.findAll("div", {"class":"at_contents"})
                # print("nameList",nameList)
                # titles = bsObj.findAll("h1", {"id": "article_title"})
                # published_time = bsObj.find('em').get_text()
                article_result = ""
                # title = ""
                #
                # for buf in titles:
                #     # print(title.get_text())
                #     title = buf.get_text()
                # # print("title",title)
                #
                # p_time = published_time[5:]

                for name in nameList:
                    article_result += name.getText().strip().replace("\n", "")
                    print("!")
                    print(article_result)
                    # print("article_result =", article_result)

                # if (title is not ""):
                #     self.mq.insert_data(str(1), title, "경향신문", article_result, url, p_time)

                return bsObj.find().findAll("a", href=re.compile("^(/NWS_Web/View/at_pg.aspx[/?])((?!mini).)*$"))

        if self.tendency == "progressivism":

            links1 = getLinks(self.progressiveArticle[self.progressive[0]], 0)
            for i in range(10):
                 newArticle1 = links1[random.randint(0, len(links1) - 1)].attrs["href"]
                 links1 = getLinks(newArticle1, 0)

            links2 = getLinks(self.progressiveArticle[self.progressive[1]], 1)
            for i in range(10):
                 newArticle2 = links2[random.randint(0, len(links2) - 1)].attrs["href"]
                 links2 = getLinks(newArticle2[23:], 1)

            links3 = getLinks(self.progressiveArticle[self.progressive[2]], 2)
            for i in range(2):
                 newArticle3 = links3[random.randint(0, len(links3) - 1)].attrs["href"]
                 links3 = getLinks(newArticle3, 2)


        elif self.status == "conservatism":
            pass


        # elif self.status == "conservatism":
        #     pass




