import aiohttp
import asyncio
import requests
from lxml import etree


@asyncio.coroutine
def get(*args, **kwargs):
    """
    A wrapper method for aiohttp's get method. Taken from Georges Dubus' article at
    http://compiletoi.net/fast-scraping-in-python-with-asyncio.html
    """

    response = yield from aiohttp.request('GET', *args, **kwargs)
    return (yield from response.read())


@asyncio.coroutine
def extract_text(url, sem):
    """
    Given the url for a chapter, extract the relevant text from it
    :param url: the url for the chapter to scrape
    :return: a string containing the chapter's text
    """
    with (yield from sem):
        page = yield from get(url)

    tree = etree.HTML(page)
    paragraphs = tree.findall('.//*/div[@class="entry-content"]/p')[1:-1]
    return url, b'\n'.join(map(etree.tostring, paragraphs))


def generate_links():
    """
    Generate the links to each of the chapters
    :return: A list of strings containing every url to visit
    """
    start_url = 'https://twigserial.wordpress.com/'
    base_url = start_url + 'category/story/'
    tree = etree.HTML(requests.get(start_url).text)
    xpath = './/*/option[@class="level-2"]/text()'
    return [base_url + suffix.strip() for suffix in tree.xpath(xpath)]


@asyncio.coroutine
def run(links):
    sem = asyncio.Semaphore(5)
    fetchers = [extract_text(link, sem) for link in links]
    return [(yield from f) for f in asyncio.as_completed(fetchers)]


def main():
    loop = asyncio.get_event_loop()
    chapters = loop.run_until_complete(run(generate_links()))
    print(len(chapters))


if __name__ == '__main__':
    main()