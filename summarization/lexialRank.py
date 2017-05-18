from __future__ import unicode_literals
from lexrankr import LexRank
from crawler.mysqlDB import mysqlDB
from example_code.clockdeco_param import clock

class LexRankforSummarization():

    def __init__(self):

        self.lexrank = LexRank(min_keyword_length=0, no_below_word_count=0, min_cluster_size=1)

    def test_summarized(self, text):
        self.lexrank.summarize(text)
        summaries = self.lexrank.probe(3)
        #self.assertEqual(len(summaries), 4)
        result = []
        for summary in summaries:
            result.append(summary)
        return result


@clock('{name}({args}) dt={elapsed:0.3f}s')
def getSummarizedArticleUsingLexialRank(keyword, tendency):
    mq = mysqlDB()
    titles = ''
    for title in mq.getTitleData(keyword, tendency):
        title = title[0]
        titles += title + ".  "
    # print("----", titles)
    LRS = LexRankforSummarization()
    summaries = LRS.test_summarized(titles)
    selectedArticles = []
    summarizedArticles = []
    # print("summaries -----", summaries)
    cnt = 0
    for summary in summaries:
        article = mq.getArticleData(summary[1:]) # summary[0] = ' '
        article = article[0][0]
        article = ((article.replace('.', '.  ')).replace('·', ' ')).strip()
        selectedArticles.append(article)
        s = "C:/Users/soicem/Desktop/robot_journalism/summarization/%d.txt"

        cnt += 1
        with open(s%cnt, 'w') as f:
            f.write(article)

    # print("-------------------selectedArticles", selectedArticles)
    for selectedArticle in selectedArticles:
        summarizedArticle = LRS.test_summarized(selectedArticle)
        # print(summarizedArticle)
        summarizedArticles.append(summarizedArticle )
    print(summarizedArticles)
    return summarizedArticles

