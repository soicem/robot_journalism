from urllib.request import urlopen
from bs4 import BeautifulSoup
import datetime
import random
import re
from example_code.coroutine.clockdeco_param import clock

random.seed(datetime.datetime.now())

def start(pageUrl):
    def getUrl(articleUrl):
        html = urlopen("http://en.wikipedia.org" + articleUrl)
        return html

    def getLinks(articleUrl):
        html = getUrl(articleUrl)
        bsObj = BeautifulSoup(html, "html.parser")
        return bsObj.find().findAll("a", href=re.compile("^(/wiki/)((?!:).)*$"))

    links = getLinks(pageUrl)
    for _ in range(20):
        newArticle = links[random.randint(0, len(links)-1)].attrs["href"]
        print(newArticle)
        links = getLinks(newArticle)

targets = ['/wiki/Marine_Le_Pen', '/wiki/Main_Page', '/wiki/Library_of_Congress_Classification']

@clock('{name}({args}) dt={elapsed:0.3f}s')
def timecheck(count):
    for _ in range(count):
        for target in targets:
            start(target)
timecheck(5)