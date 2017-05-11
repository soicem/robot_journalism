from crawler.Article import *
import asyncio
import socket

from example_code.clockdeco_param import clock
from summarization.lexialRank import getSummarizedArticleUsingLexialRank

@clock('{name}({args}) dt={elapsed:0.3f}s')
def crawlingWeb(tendency,keyword):
    ar2 = Article(tendency, keyword)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(ar2.gathering(loop))

def getTendency_Keyword():
    # create a socket object
    print("waiting client connection...")
    serversocket = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM)

    # get local machine name
    host = socket.gethostname()

    port = 8090

    # bind to the port
    serversocket.bind((host, port))

    # queue up to 5 requests
    serversocket.listen(5)


    # establish a connection
    clientsocket, addr = serversocket.accept()
    msg = clientsocket.recv(1024)
    result = msg.decode('utf8').split(',')
    print("Got a connection from %s" % str(addr))

    clientsocket.close()
    return (result[0],result[1])

def saveSummarizedArticleIntoMySQL(keyword, tendency, summarizedArticles):
    mq = mysqlDB()
    for summarizedArticle in summarizedArticles:
        mq.insertDataIntoSummarizedArticles(tendency, keyword, summarizedArticle)
    mq.mysql_close()

if __name__=="__main__":
    result = getTendency_Keyword()
    keyword, tendency = result
    print(result)
    crawlingWeb(tendency,keyword)
    summarizedArticles = []
    for summarizedArticle3 in getSummarizedArticleUsingLexialRank():
        summarizedArticles.append((summarizedArticle3[0] + '\n' + summarizedArticle3[1] + '\n' + summarizedArticle3[2]))
    saveSummarizedArticleIntoMySQL(keyword, tendency, summarizedArticles)



