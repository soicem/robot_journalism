from urllib.request import urlopen
from bs4 import BeautifulSoup
import datetime
import random
import re
import aiohttp

from crawler.mysqlDB import *

class Article():
    def __init__(self, keyword, tendency):
        self.mq = mysqlDB()
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
        self.conservative = ["동아일보", "중앙일보", "조선일보"]
        self.conservatismTargets = {
            self.conservative[0]: "http://news.donga.com/",
            self.conservative[1]: "http://news.joins.com/",
            self.conservative[2]: "http://www.chosun.com/"
        }
        self.conservativeArticle = {
            self.conservative[0]: "/Politics/",
            self.conservative[1]: "/politics/",
            self.conservative[2]: "/politics/"
        }

        self.url_list=[]

        self.conservative = []
        self.conservatismTargets = {}

        random.seed(datetime.datetime.now())

    async def fetch(self,client, articleUrl,i):
        url  = self.progressivismTargets[self.progressive[i]] + articleUrl
        async with client.get(url) as resp:
            assert resp.status == 200
            return await resp.text()

    async def gathering(self,loop):
        async def getInfo(articleUrl):
            if self.tendency == "progressivism":
                if articleUrl.find("/arti/politics/") > -1:
                    i = 0
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
                    i = 1
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
                    i = 2
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

                    published_times = bsObj.find("div", {"class": "info_data"})
                    if published_times != None:
                        p_time = published_times.get_text()[:14]

                    if (title is not ""):
                        self.mq.insert_data(str(1), title, "오마이뉴스", article_result, url, p_time)

            elif self.tendency == "conservatism":
                if articleUrl.find("donga") > -1:
                    i = 0
                    url = articleUrl
                    html = urlopen(url)
                    bsObj = BeautifulSoup(html, "html.parser")
                    nameList = bsObj.findAll("div", {"class": "article_txt"})
                    article_result = ""
                    p_time = ""

                    for name in nameList:  article_result += name.getText().strip().replace("\n", "")

                    title = bsObj.find("h2", {"class": "title"}).get_text()

                    published_times = bsObj.find_all('meta', attrs={'property': 'article:published_time'})
                    for published_time in published_times:
                        p_date = re.compile(
                            r'(\d{1,4}[/-]\d{1,2}[/-]\d{1,2}[T]\d{1,2}[/:]\d{1,2}[/:]\d{1,2}[+]\d{1,2}[/-:]\d{1,2})')
                        p_time = p_date.findall(str(published_time))

                    if (title is not ""):
                        p_time = (p_time[0])[0:10] + " " + (p_time[0])[11:19]
                        self.mq.insert_data(str(2), title, "동아일보", article_result, url, p_time)

                if articleUrl.find("/article/") > -1:
                    i = 1
                    url = self.conservatismTargets[self.conservative[i]] + articleUrl
                    html = urlopen(url)
                    bsObj = BeautifulSoup(html, "html.parser")
                    nameList = bsObj.findAll("div", {"id": "article_body"})
                    article_result = ""
                    p_time = ""

                    for name in nameList:  article_result += name.getText().strip().replace("\n", "")

                    title = bsObj.find("title").get_text()


                    published_times = bsObj.find_all('meta', attrs={'property': 'article:published_time'})
                    for published_time in published_times:
                        p_date = re.compile(
                            r'(\d{1,4}[/-]\d{1,2}[/-]\d{1,2}[T]\d{1,2}[/:]\d{1,2}[/:]\d{1,2}[+]\d{1,2}[/-:]\d{1,2})')
                        p_time = p_date.findall(str(published_time))

                    if (title is not ""):
                        p_time = (p_time[0])[0:10] + " " + (p_time[0])[11:19]
                        self.mq.insert_data(str(2), title, "중앙일보", article_result, url, p_time)

                if articleUrl.find("/news.chosun.com/") > -1:
                    i = 2
                    url =  articleUrl
                    html = urlopen(url)
                    bsObj = BeautifulSoup(html, "html.parser")
                    nameList = bsObj.findAll("div", {"class": "par"})
                    article_result = ""

                    for name in nameList:  article_result += name.getText().strip().replace("\n", "")

                    title = bsObj.find("h1",{"id":"news_title_text_id"}).get_text()
                    p_time = bsObj.find('div', attrs={'class': 'news_date'}).get_text().strip()[5:21]

                    if (title is not ""):
                        self.mq.insert_data(str(2), title, "조선일보", article_result, url, p_time)

        async def getLinks(articleUrl, i):
            async with aiohttp.ClientSession() as client:
                url = await self.fetch(client, articleUrl,i)
                bsObj = BeautifulSoup(url, "html.parser")

            link_list = set() #같은 주소 제거 오마이뉴스는 링크다른데 중복기사 있음
            if self.tendency == "progressivism":
                if i == 0:  # 0 : 한겨례
                    han_links = bsObj.findAll("a", href=re.compile("^(/arti/politics/)((?!:).)*$"))
                    for link in han_links:
                        if link.get_text().find(self.keyword) > -1:
                            link = link.get('href')
                            link_list.add(link)

                elif i == 1:  # 경향신문추가
                    khan_links = bsObj.findAll("a", href=re.compile("khan_art_view.html[/?]artid=2017"))
                    for link in khan_links:
                        if link.get_text().find(self.keyword) > -1:
                            link = link.get('href')[23:]
                            link_list.add(link)

                elif i == 2:  # 오마이뉴스 추가
                    ohmy_links = bsObj.findAll("a", href=re.compile(
                        "^(/NWS_Web/View/at_pg.aspx[/?]CNTN_CD=A00023)((?!mini).)*$"))  # 링크주소 수시로 바뀜
                    for link in ohmy_links:
                        if link.get_text().find(self.keyword) > -1:
                            link = link.get('href')
                            link_list.add(link)

            if self.tendency == "conservatism":
                if i == 0 : # 동아일보
                    donga_links = bsObj.findAll("a",href=re.compile("news.donga.com/Politics/3/00"))
                    for link in donga_links:
                        if link.get_text().find(self.keyword) > -1:
                            link = link.get('href')
                            link_list.add(link)
                elif i == 1 : # 중앙일보
                    joongang_links = bsObj.findAll("a", href=re.compile("^(/article/)"))
                    for link in joongang_links:
                        if link.get_text().find(self.keyword) > -1:
                            link = link.get('href')
                            link_list.add(link)
                elif i == 2 : # 조선일보
                    chosun_links = bsObj.findAll("a", href=re.compile("^(http://news.chosun.com/site/data/html_dir/)"))
                    for link in chosun_links:
                        if link.get_text().find(self.keyword) > -1:
                            link = link.get('href')
                            link_list.add(link)
            self.url_list.extend(list(link_list))

        if self.tendency == "progressivism":
            for i in range(3):
                await getLinks(self.progressiveArticle[self.progressive[i]], i)

            for i in range(len(self.url_list)):
                link = self.url_list[random.randint(0, len(self.url_list) - 1)]
                await getInfo(link)
                self.url_list.remove(link)

        elif self.status == "conservatism":
            for i in range(3):
                await getLinks(self.conservativeArticle[self.conservative[i]], i)

            for i in range(len(self.url_list)):
                link = self.url_list[random.randint(0, len(self.url_list) - 1)]
                await getInfo(link)
                self.url_list.remove(link)
