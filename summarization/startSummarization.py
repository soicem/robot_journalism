# from crawler.mysqlDB import mysqlDB
# from summarization.lexialRank import getSummarizedArticleUsingLexialRank
#
# def makeSummarizedArticle(result):
#     keyword, tendency = result
#     mq = mysqlDB()
#     summarizedArticles = []
#     bufArticles, titles, imgs = getSummarizedArticleUsingLexialRank(keyword, tendency)
#     # bufArticles, titles =getSummarizedArticleUsingLexialRank(keyword, tendency)
#     titleCnt = 0
#     ##이미지 저장테이블만들기
#     for summarizedArticle3 in bufArticles:
#         buf = summarizedArticle3[0]
#         for i in range(len(summarizedArticle3)-1):
#             buf += '\n' + summarizedArticle3[i+1]
#         summarizedArticles.append(buf)
#         mq.insertDataIntoSummarizedArticles(tendency, keyword, titles[titleCnt], buf)
#         titleCnt += 1
#
#     return summarizedArticles,titles
from crawler.mysqlDB import mysqlDB
from summarization.lexialRank import getSummarizedArticleUsingLexialRank

def makeSummarizedArticle(result):
    keyword, tendency = result
    mq = mysqlDB()
    summarizedArticles = []
    bufArticles, titles, imgUrls = getSummarizedArticleUsingLexialRank(keyword, tendency)

    titleCnt = 0
    for summarizedArticle3 in bufArticles:
        buf = summarizedArticle3[0]
        for i in range(len(summarizedArticle3)-1):
            buf += '\n' + summarizedArticle3[i+1]
        summarizedArticles.append(buf)
        # mq.insertDataIntoSummarizedArticles(tendency, keyword, titles[titleCnt], buf,imgUrls[titleCnt])
        mq.insertDataIntoSummarizedArticles(tendency, keyword, titles[titleCnt], buf, imgUrls[titleCnt])
        titleCnt += 1

    return titles, summarizedArticles, imgUrls
