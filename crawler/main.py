from crawler.Article import *
import asyncio

from example_code.clockdeco_param import clock

@clock('{name}({args}) dt={elapsed:0.3f}s')
def main(tendency,keyword):
    ar2 = Article.Article(tendency, keyword)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(ar2.gathering(loop))


if __name__=="__main__":
    tendency = input("tendency : ")
    keyword = input("keyword : ")
    main(tendency,keyword)


