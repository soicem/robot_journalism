"""Download flags of top 20 countries by population

asyncio + aiottp version

Sample run::

    $ python3 flags_asyncio.py
    EG VN IN TR RU ID US DE CN MX JP BD NG ET FR BR PH PK CD IR
    20 flags downloaded in 1.07s

"""
# BEGIN FLAGS_ASYNCIO
import asyncio
import aiohttp  # <1>

from bs4 import BeautifulSoup

from example_code.coroutine.flags import BASE_URL, save_flag, show, main  # <2>


@asyncio.coroutine  # <3>
def get_link(url):
    resp = yield from aiohttp.request('GET', url)  # <4>
    return resp


@asyncio.coroutine
def download_one(cc):  # <6>
    resp = yield from get_link(cc)  # <7>
    print(resp)
    return cc


def download_many(urlist):
    loop = asyncio.get_event_loop()  # <8>
    to_do = [download_one(cc) for cc in urlist]  # <9>
    wait_coro = asyncio.wait(to_do)  # <10>
    res, _ = loop.run_until_complete(wait_coro)  # <11>
    loop.close() # <12>
    return res


if __name__ == '__main__':
    urllist = ['http://www.daum.net', 'http://www.naver.com']
    print(download_many(urllist))
# END FLAGS_ASYNCIO
