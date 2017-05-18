from urllib.request import urlopen
from bs4 import BeautifulSoup
import datetime
import random
import re

import asyncio
import aiohttp  # <1>
import asyncio
import bs4
import tqdm

class Article():
    def __init__(self, tendency, keyword):

        self.keyword = keyword # specific keyword related to politic
        self.tendency = tendency
        self.progressive = ["한겨례", "경향신문", "오마이뉴스"]
        self.progressivismTargets = {
            self.progressive[0]: "http://www.hani.co.kr/"}
            # self.progressive[1]: "http://news.khan.co.kr/",
            # self.progressive[2]: "http://www.ohmynews.com/"}
        self.progressiveArticle = {
            self.progressive[0]: "/arti/politics/",
            self.progressive[1]: "/kh_politics/",
            self.progressive[2]: "/NWS_Web/ArticlePage/Total_Article.aspx?PAGE_CD=C0400"
        }
        self.conservative = []
        self.conservatismTargets = {}

        self.visitedUrl = []

        random.seed(datetime.datetime.now())

    @asyncio.coroutine
    def gathering(self, target):

        def getLinks(target, articleUrl):
            url = target + articleUrl
            resp = yield from self.get_link(url)
            bsObj =BeautifulSoup(resp, "lxml")

            if target is "http://www.hani.co.kr/": # : 한겨례
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

                return bsObj.find().findAll("a", href=re.compile("^(/arti/politics/)((?!:).)*$"))

        newArticle1 = ''
        for _ in range(10):
            links1 = yield from getLinks(target, newArticle1)
            newArticle1 = links1[random.randint(0, len(links1) - 1)].attrs["href"]
            print(newArticle1)

    @asyncio.coroutine  # <3>
    def get_link(self, url):
        resp = yield from aiohttp.request('GET', url)  # <4>
        #resp = yield from resp.text()
        return resp.text()

    @asyncio.coroutine
    def decision(self, target):  # <6>
        #resp = yield from self.get_link(target)  # <7>
        #soup = bs4.BeautifulSoup(resp)
        yield from self.gathering(target)
        return

    def start(self):
        loop = asyncio.get_event_loop()  # <8>
        to_do = [self.decision(target) for target in self.progressivismTargets.values()]  # <9>
        wait_coro = asyncio.wait(to_do)  # <10>
        res, _ = loop.run_until_complete(wait_coro)  # <11>
        loop.close()  # <12>
        return res

ar = Article('progressivism', "문재인")
ar.start()