from __future__ import unicode_literals
from lexrankr import LexRank
from crawler.mysqlDB import mysqlDB
from example_code.clockdeco_param import clock

class LexRankforSummarization():

    def __init__(self):

        self.lexrank = LexRank(min_keyword_length=0, no_below_word_count=0, min_cluster_size=1)

    def test_summarized(self, text):
        self.lexrank.summarize(text)
        try:
            summaries = self.lexrank.probe(3)
        except:
            summaries = self.lexrank.probe(2)
        result = []
        for summary in summaries:
            result.append(summary)
        # print("result",result)
        return result

@clock('{name}({args}) dt={elapsed:0.3f}s')
def getSummarizedArticleUsingLexialRank(keyword, tendency):
    mq = mysqlDB()
    titles = []
    titleSet = ''
    for title in mq.getTitleData(keyword, tendency):
        title = title[0]
        titles.append(title)
        titleSet += title + '.  '
    LRS = LexRankforSummarization()
    # print("title",titleSet)
    summaries = LRS.test_summarized(titleSet)
    selectedArticles = []
    summarizedArticles = []
    imgs = []
    article_urls = []

    print("summaries", summaries)

    for summary in summaries:
        # article = mq.getArticleData(summary.strip()) # summary[0] = ' '
        contents = mq.getArticleData(summary.strip())  # summary[0] = ' '
        try:
            article = contents[0][0]
            img = contents[0][1]
            article = ((article.replace('.', '.  ')).replace('·', ' ')).strip()
            selectedArticles.append(article)
            imgs.append(img)
        except:
            print("일치하는 제목이없습니다.")

    print("selectedArticles", selectedArticles)

    for selectedArticle in selectedArticles:
        summarizedArticle = LRS.test_summarized(selectedArticle)
        summarizedArticles.append(summarizedArticle )
    return summarizedArticles, summaries,imgs
    # return summarizedArticles, titles

