from urllib.request import urlopen
from bs4 import BeautifulSoup
import datetime
import random
import re

from example_code.coroutine.clockdeco_param import clock

progressivismTargets = {
    "한겨례" : "http://www.hani.co.kr/",
    "경향신문" : "http://www.khan.co.kr/",
    "오마이뉴스" : "http://www.ohmynews.com/"}
conservatismTargets = {}

random.seed(datetime.datetime.now())
def getLinks(articleUrl):
    html = urlopen("http://www.hani.co.kr/"+articleUrl)
    bsObj = BeautifulSoup(html, "html.parser")
    return bsObj.find().findAll("a", href=re.compile("^(/arti/politics/)((?!:).)*$"))
links = getLinks("/arti/politics/")
while len(links) > 0:
    newArticle = links[random.randint(0, len(links)-1)].attrs["href"]
    print(newArticle)
    links = getLinks(newArticle)

