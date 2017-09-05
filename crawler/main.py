from summarization.startSummarization import makeSummarizedArticle
from connectionCode.connectiWithDjango import socket_Django
from crawler.startCrawl import crawlingWeb

if __name__=="__main__":
    while(True):
        socket = socket_Django()
        result = socket.getTendency_Keyword() # return to (keyword, tendency)
        print(result)
        crawlingWeb(result)
        titles, summarized_articles, imgUrls = makeSummarizedArticle(result)
        socket.send_Newdata(titles, summarized_articles, imgUrls)
        socket.socketClose()
