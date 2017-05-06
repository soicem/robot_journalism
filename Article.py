from urllib.request import urlopen
from bs4 import BeautifulSoup
import datetime
import random
import re

from robot_journalism import mysqlDB

class Article():
    def __init__(self, tendency, keyword):
        self.mq = mysqlDB.mysqlDB()
        self.tendency = tendency
        self.keyword = keyword
        self.progressive = ["한겨례", "경향신문", "오마이뉴스"]
        self.progressivismTargets = {
            self.progressive[0]: "http://www.hani.co.kr/",
            self.progressive[1]: "http://news.khan.co.kr/",
            self.progressive[2]: "http://www.ohmynews.com/"}
        self.progressiveArticle = {
            self.progressive[0]: "/arti/politics/",
            self.progressive[1]: "/kh_politics/", #추가
            self.progressive[2]: "/NWS_Web/ArticlePage/Total_Article.aspx?PAGE_CD=C0400" #추가
        }
        self.url_list=[]
        self.conservative = []
        self.conservatismTargets = {}

        random.seed(datetime.datetime.now())

    def gathering(self):
        def getInfo(articleUrl):
            print("url :", articleUrl)
            if articleUrl.find("/arti/politics/") > -1:
                i=0
                url = self.progressivismTargets[self.progressive[i]] + articleUrl
                html = urlopen(url)
                bsObj = BeautifulSoup(html, "html.parser")
                nameList = bsObj.findAll("div", {"class": "text"})
                titles = bsObj.findAll("span", {"class": "title"})
                published_times = bsObj.find_all('meta', attrs={'property': 'article:published_time'})
                article_result = ""
                title = ""

                for buf in titles:
                    title = buf.get_text()
                p_time = ""

                for published_time in published_times:
                    p_date = re.compile(
                        r'(\d{1,4}[/-]\d{1,2}[/-]\d{1,2}[T]\d{1,2}[/:]\d{1,2}[/:]\d{1,2}[+]\d{1,2}[/-:]\d{1,2})')
                    p_time = p_date.findall(str(published_time))

                for name in nameList:  article_result += name.getText().strip().replace("\n", "")

                if (title is not ""):
                    p_time = (p_time[0])[0:10] + " " + (p_time[0])[11:19]
                    self.mq.insert_data(str(1), title, "한겨례", article_result, url, p_time)

            elif articleUrl.find("khan_art_view") > -1:
                i=1
                url = self.progressivismTargets[self.progressive[i]] + articleUrl
                html = urlopen(url)
                bsObj = BeautifulSoup(html, "html.parser")
                nameList = bsObj.findAll("p", {"class": "content_text"})
                titles = bsObj.findAll("h1", {"id": "article_title"})
                published_time = bsObj.find('em').get_text()
                article_result = ""
                title = ""

                for buf in titles:
                    title = buf.get_text()

                p_time = published_time[5:]

                for name in nameList:  article_result += name.getText().strip().replace("\n", "")

                if (title is not ""):
                    self.mq.insert_data(str(1), title, "경향신문", article_result, url, p_time)

            elif articleUrl.find("/NWS_Web/View") > -1:
                i=2
                url = self.progressivismTargets[self.progressive[i]] + articleUrl
                html = urlopen(url)
                bsObj = BeautifulSoup(html, "html.parser")
                nameList = bsObj.findAll("div", {"class": "at_contents"})
                article_result = ''
                p_time = ''
                title = ""
                for name in nameList:
                    article_result += name.getText().strip().replace("\n", "")

                titles = bsObj.find("h3", {"class": "tit_subject"})
                if titles != None:
                    title = titles.get_text()
                    # print("title", title)

                published_times = bsObj.find("div", {"class": "info_data"})
                if published_times != None:
                    p_time = published_times.get_text()[:14]

                if (title is not ""):
                    self.mq.insert_data(str(1), title, "오마이뉴스", article_result, url, p_time)

        def getLinks(articleUrl, i):
            url = self.progressivismTargets[self.progressive[i]] + articleUrl
            html = urlopen(url)
            bsObj = BeautifulSoup(html, "html.parser")

            if i == 0: # 0 : 한겨례
                han_links = bsObj.findAll("a", href=re.compile("^(/arti/politics/)((?!:).)*$"))
                link_list = []
                for link in han_links:
                    if link.get_text().find(self.keyword) > -1:
                        link = link.get('href')
                        link_list.append(link)
                return link_list # 안철수가 들어간 링크만 보냄

            elif i == 1:  # 경향신문추가
                khan_links = bsObj.findAll("a", href=re.compile("khan_art_view.html[/?]artid=2017"))
                link_list = []
                for link in khan_links:
                    if link.get_text().find(self.keyword) > -1:
                        link = link.get('href')[23:]
                        link_list.append(link)
                return link_list

            elif i == 2:  # 오마이뉴스 추가
                ohmy_links = bsObj.findAll("a", href=re.compile("^(/NWS_Web/View/at_pg.aspx[/?]CNTN_CD=A00023)((?!mini).)*$"))#링크주소 수시로 바뀜
                link_list = []
                for link in ohmy_links:
                    if link.get_text().find(self.keyword) > -1:
                        link = link.get('href')
                        link_list.append(link)
                return link_list

        if self.tendency == "progressivism":

            self.url_list.append(getLinks(self.progressiveArticle[self.progressive[0]], 0))
            self.url_list.append(getLinks(self.progressiveArticle[self.progressive[1]], 1))
            self.url_list.append(getLinks(self.progressiveArticle[self.progressive[2]], 2))

            for i in range(20):
                newSite = self.url_list[random.randint(0, len(self.url_list) - 1)] # 한겨례, 경향신문, 오마이뉴스중 선택
                getInfo(newSite[random.randint(0, len(newSite) - 1)])

        elif self.status == "conservatism":
            pass