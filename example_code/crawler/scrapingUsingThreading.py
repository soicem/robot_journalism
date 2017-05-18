from bs4 import BeautifulSoup
import datetime
import random
import re
import requests
from enum import Enum
from concurrent import futures

from example_code.coroutine.clockdeco_param import clock

random.seed(datetime.datetime.now())
def start(pageUrl):

    def getLinks(pageUrl):
        resp = requests.get("http://en.wikipedia.org"+ pageUrl)
        bsObj = BeautifulSoup(resp.text, "html.parser")
        return bsObj.find().findAll("a", href=re.compile("^(/wiki/)((?!:).)*$"))
    links = getLinks(pageUrl)
    for _ in range(20):
        newArticle = links[random.randint(0, len(links)-1)].attrs["href"]
        print(newArticle)
        links = getLinks(newArticle)
    return "soicem"


def download_many():
    distros = ['/wiki/Marine_Le_Pen', '/wiki/Main_Page', '/wiki/Library_of_Congress_Classification']
    workers = min(20, len(distros))  # <4>
    #counter = collections.Counter(distros)
    with futures.ThreadPoolExecutor(workers) as executor:  # <5>
        #res = executor.map(start, distros)  # <6>
        to_do_map = {}
        for distro in distros:
            future = executor.submit(start, distro)
            to_do_map[future] = distro
        to_do_iter = futures.as_completed(to_do_map)

        for future in to_do_iter:
            HTTPStatus = Enum('Status', 'ok not_found error')
            try:
                res = future.result()
            except requests.exceptions.HTTPError as exc:
                error_msg = 'HTTP {res.status_code} - {res.reason}'
                error_msg = error_msg.format(res=exc.response)
            except requests.exceptions.ConnectionError as exc:
                error_msg = 'Connection error'
            else:
                error_msg = ''
                # status = res.status

            # if error_msg:
            #     status = HTTPStatus.error
            # if error_msg:
            #     cc = to_do_map[future]
            #     print('*** Error for {}: {}'.format(cc, error_msg))

    return len(list(to_do_map))


@clock('{name}({args}) dt={elapsed:0.3f}s')
def loop(count):
    for _ in range(count):
        download_many()

if __name__ == '__main__':
    loop(5)