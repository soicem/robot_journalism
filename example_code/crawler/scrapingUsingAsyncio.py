import aiohttp
import asyncio
from bs4 import BeautifulSoup

import datetime
import random
import re
import tqdm

from example_code.coroutine.clockdeco_param import clock

async def fetch(client, articleUrl):
    async with client.get('https://en.wikipedia.org' + articleUrl) as resp:
        assert resp.status == 200
        return (await resp.text())

async def getLinks(articleUrl):
    async with aiohttp.ClientSession() as client:
        html = await fetch(client, articleUrl)
        bs_obj = BeautifulSoup(html, "html.parser")
        print(bs_obj.title.get_text())
        return bs_obj.find().findAll("a", href=re.compile("^(/wiki/)((?!:).)*$"))

@asyncio.coroutine
def wait_with_progress(coros):
    for f in tqdm.tqdm(asyncio.as_completed(coros)):
        yield from f

@asyncio.coroutine
def start(articleUrl):
    links = yield from getLinks(articleUrl)
    for _ in range(20):
        newArticle = links[random.randint(0, len(links) - 1)].attrs["href"]
        links = yield from getLinks(newArticle)

@clock('{name}({args}) dt={elapsed:0.3f}s')
def main(count):
    random.seed(datetime.datetime.now())
    for _ in range(count):
        targets = ['/wiki/Marine_Le_Pen', '/wiki/Main_Page', '/wiki/Library_of_Congress_Classification']
        loop = asyncio.get_event_loop()
        f = asyncio.wait([start(target) for target in targets])
        loop.run_until_complete(f)

if __name__ == '__main__':
    main(1)