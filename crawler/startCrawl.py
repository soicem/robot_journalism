import asyncio
from crawler.Article import Article
from example_code.clockdeco_param import clock

@clock('{name}({args}) dt={elapsed:0.3f}s')
def crawlingWeb(result):
    keyword, tendency = result
    ar = Article(keyword, tendency)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(ar.gathering(loop))

