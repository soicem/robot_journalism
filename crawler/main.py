from summarization.startSummarization import makeSummarizedArticle
from connectionCode.connectiWithDjango import getTendency_Keyword
from crawler.startCrawl import crawlingWeb

if __name__=="__main__":
    while(True):
        result = getTendency_Keyword() # return to (keyword, tendency)
        print(result)
        crawlingWeb(result)
        makeSummarizedArticle(result)



