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
        self.url_list = []
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

        self.conservative = ["동아일보", "중앙일보", "조선일보"]
        self.conservatismTargets = {
            self.conservative[0]: "http://news.donga.com/",
            self.conservative[1]: "http://news.joins.com",
            self.conservative[2]: "http://www.chosun.com/"
        }
        self.conservativeArticle = {
            self.conservative[0]: "/Politics/",
            self.conservative[1]: "/politics/",
            self.conservative[2]: "/politics/"
        }

        random.seed(datetime.datetime.now())

    async def fetch(self,client, articleUrl,i):
        if self.tendency == "progressivism":
            url = self.progressivismTargets[self.progressive[i]] + articleUrl

        elif self.tendency == "conservatism":
            url = self.conservatismTargets[self.conservative[i]] + articleUrl

        async with client.get(url) as resp:
            assert resp.status == 200
            return await resp.text()

    async def gathering(self,loop):
        async def getInfo(articleUrl,html):
            article_result = ""
            img = ""
            p_time = ""
            i=0
            bsObj = BeautifulSoup(html, "html.parser")
            img_urls = bsObj.findAll("img")

            if self.tendency == "progressivism":
                if articleUrl.find("/arti/politics/") > -1:
                    i=0  #한겨례
                    url = self.progressivismTargets[self.progressive[i]]+articleUrl
                    title = bsObj.find("span", {"class": "title"})
                    nameList = bsObj.findAll("div", {"class": "text"})
                    published_times = bsObj.find_all('meta', attrs={'property': 'article:published_time'})

                    for published_time in published_times:
                        p_date = re.compile(
                            r'(\d{1,4}[/-]\d{1,2}[/-]\d{1,2}[T]\d{1,2}[/:]\d{1,2}[/:]\d{1,2}[+]\d{1,2}[/-:]\d{1,2})')
                        p_time = p_date.findall(str(published_time))

                    p_time = (p_time[0])[0:10] + " " + (p_time[0])[11:19]


                elif articleUrl.find("khan_art_view") > -1:
                    i = 1  # 경향신문
                    url = self.progressivismTargets[self.progressive[i]] + articleUrl
                    title = bsObj.find("h1", {"id": "article_title"})
                    nameList = bsObj.findAll("p", {"class": "content_text"})
                    if title != None:
                        published_time = bsObj.find('em').get_text()
                        p_time = published_time[5:].replace(".","-")


                elif articleUrl.find("/NWS_Web/View") > -1:
                    i = 2  # 오마이뉴스
                    url = self.progressivismTargets[self.progressive[i]] + articleUrl
                    nameList = bsObj.findAll("div", {"class": "at_contents"})#태그 계속 바뀐다
                    title = bsObj.find("h3", {"class": "tit_subject"})
                    published_time = bsObj.find("div", {"class": "info_data"})

                    if published_time != None:
                        p_time = published_time.get_text()[:15].replace("\n","").replace(".","-")
                        p_time = "20"+p_time+":00"

                for img_url in img_urls:
                    if img_url:
                        img_url = img_url.get("src")
                        if img_url.find("http://img.hani.co.kr/imgdb")>-1 or img_url.find("http://img.khan.co.kr/news/2") > -1 \
                                or img_url.find("STD_IMG_FILE") > -1:
                            img = img_url

            elif self.tendency == "conservatism":
                if articleUrl.find("Politics") > -1:
                    i=0 #동아일보
                    url = self.conservatismTargets[self.conservative[i]] + articleUrl
                    nameList = bsObj.findAll("div", {"class": "article_txt"})
                    title = bsObj.find("h2", {"class": "title"}).get_text()
                    published_times = bsObj.find_all('meta', attrs={'property': 'article:published_time'})

                    for published_time in published_times:
                        p_date = re.compile(
                            r'(\d{1,4}[/-]\d{1,2}[/-]\d{1,2}[T]\d{1,2}[/:]\d{1,2}[/:]\d{1,2}[+]\d{1,2}[/-:]\d{1,2})')
                        p_time = p_date.findall(str(published_time))
                    p_time = (p_time[0])[0:10] + " " + (p_time[0])[11:19]

                if articleUrl.find("/article/") > -1:
                    i = 1  # 중앙일보
                    url = self.conservatismTargets[self.conservative[i]] + articleUrl
                    nameList = bsObj.findAll("div", {"id": "article_body"})
                    title = bsObj.find("title").get_text()
                    published_times = bsObj.find_all('meta', attrs={'property': 'article:published_time'})
                    for published_time in published_times:
                        p_date = re.compile(
                            r'(\d{1,4}[/-]\d{1,2}[/-]\d{1,2}[T]\d{1,2}[/:]\d{1,2}[/:]\d{1,2}[+]\d{1,2}[/-:]\d{1,2})')
                        p_time = p_date.findall(str(published_time))

                    p_time = (p_time[0])[0:10] + " " + (p_time[0])[11:19]

                if articleUrl.find("/site") > -1:
                    i = 2  # 조선일보
                    url = self.conservatismTargets[self.conservative[i]] + articleUrl
                    nameList = bsObj.findAll("div", {"class": "par"})
                    title = bsObj.find("h1",{"id":"news_title_text_id"}).get_text()
                    p_time = bsObj.find('div', attrs={'class': 'news_date'}).get_text().strip()[5:21].replace(".","-")+":00"

                for img_url in img_urls:
                    if img_url != None and i != 1:
                        img_url = img_url.get("src")
                    elif i == 1:
                        img_url = img_url.get("data-src")

                    if img_url != None:
                        if img_url.find("http://dimg.donga.com/wps/NEWS/IMAGE") > -1 or \
                                        img_url.find("news/component/htmlphoto_mmdata") > -1 or img_url.find(
                            "sitedata/image") > -1:
                            img = img_url

            for name in nameList:  article_result += name.getText().strip().replace("\n", "")
            article_result = article_result[:article_result.find('var')]

            if title != None:
                if self.tendency == "progressivism":
                    newsite = self.progressive[i]
                    title = title.get_text()
                elif self.tendency == "conservatism":
                    newsite = self.conservative[i]
                # self.mq.insertDataIntoArticles(self.tendency, self.keyword, title, "경향신문", article_result, url, p_time)
                self.mq.insertDataIntoArticles(self.tendency, self.keyword, title, newsite, article_result,
                                               url, img, p_time)

        async def getLinks(articleUrl, i):
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            }
            async with aiohttp.ClientSession(headers=headers) as client:
                url = await self.fetch(client, articleUrl,i)
                bsObj = BeautifulSoup(url, "html.parser")

            link_list = set() #같은 주소 제거 오마이뉴스는 링크다른데 중복기사 있음

            if self.tendency == "progressivism" :

                if i == 0:  # 0 : 한겨례
                    links = bsObj.findAll("a", href=re.compile("^(/arti/politics/)((?!:).)*$"))

                elif i == 1:  # 경향신문
                    links = bsObj.findAll("a", href=re.compile("khan_art_view.html[/?]artid=2017"))

                elif i == 2:  # 오마이뉴스 추가
                    links = bsObj.findAll("a", href=re.compile(
                        "^(/NWS_Web/View/at_pg.aspx[/?]CNTN_CD=A00023)((?!mini).)*$"))  # 링크주소 수시로 바뀜

            if self.tendency == "conservatism":

                if i == 0 : # 동아일보
                    links = bsObj.findAll("a", href=re.compile("news.donga.com/Politics/3/00/"))

                elif i == 1 : # 중앙일보
                    links = bsObj.findAll("a", href=re.compile("^(/article/)"))

                elif i == 2 : # 조선일보
                    links = bsObj.findAll("a", href=re.compile("^(http://news.chosun.com/site/data/html_dir/)"))

            for link in links:
                if link.get_text().find(self.keyword) > -1:
                    if self.tendency == "progressivism" and i == 1:  # 경향신문
                        link = link.get('href')[23:]
                    elif self.tendency == "conservatism" and i != 1:  # i=0 동아일보 i=2 조선일보
                        link = link.get('href')[22:]
                    else:
                        link = link.get('href')
                    link_list.add(link)

            self.url_list.extend(list(link_list))

        if self.tendency == "progressivism":
            for i in range(3):
                await getLinks(self.progressiveArticle[self.progressive[i]], i)

        elif self.tendency == "conservatism":
            for i in range(3):
                await getLinks(self.conservativeArticle[self.conservative[i]], i)

        for li in range(len(self.url_list)):
            link = self.url_list[random.randint(0, len(self.url_list) - 1)]
            i = 0
            if link.find("Politics") > -1 or link.find("/arti/politics/") > -1:
                i = 0
            elif link.find("/article/") > -1 or link.find("khan_art_view") > -1:
                i = 1
            elif link.find("/site") > -1 or link.find("/NWS_Web/View") > -1:
                i = 2
            html = await self.url_connection(link, i)
            await getInfo(link, html)
            self.url_list.remove(link)

    async def url_connection(self,link,i):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
        }
        async with aiohttp.ClientSession(headers=headers) as client:
            html = await self.fetch(client, link, i)
        return html