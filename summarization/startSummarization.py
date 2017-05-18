from crawler.mysqlDB import mysqlDB
from summarization.lexialRank import getSummarizedArticleUsingLexialRank

def saveSummarizedArticleIntoMySQL(keyword, tendency, summarizedArticles):
    mq = mysqlDB()
    for summarizedArticle in summarizedArticles:
        mq.insertDataIntoSummarizedArticles(tendency, keyword, summarizedArticle)


def makeSummarizedArticle(result):
    keyword, tendency = result

    summarizedArticles = []
    for summarizedArticle3 in getSummarizedArticleUsingLexialRank(keyword, tendency):
        buf = summarizedArticle3[0]
        for i in range(len(summarizedArticle3)-1):
            buf += '\n' + summarizedArticle3[i+1]
        summarizedArticles.append(buf)
        #summarizedArticles.append((summarizedArticle3[0] + '\n' + summarizedArticle3[1] + '\n' + summarizedArticle3[2]))
    saveSummarizedArticleIntoMySQL(keyword, tendency, summarizedArticles)