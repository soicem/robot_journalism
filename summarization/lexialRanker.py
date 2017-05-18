from __future__ import unicode_literals
from lexrankr import LexRank
from crawler.mysqlDB import *

class LexRankforSummarization():

    def __init__(self):
        self.text = "사과 배 감 귤. 배 감 귤 수박. 감 귤 수박 딸기. 오이 참외 오징어. 참외 오징어 달팽이."
        self.lexrank = LexRank(min_keyword_length=0, no_below_word_count=0, min_cluster_size=1)

    def test_summarized(self):
        self.lexrank.summarize(self.text)
        summaries = self.lexrank.probe(4)
        print(summaries)
        self.assertEqual(len(summaries), 4)

        for summary in summaries:
            print(summary)
if __name__ == '__main__':
    unittest.main()


if __name__ == '__main__':
    mq = mysqlDB()
    text = mq.getAllData()
    LRS = LexRankforSummarization(text)
    LRS.test_summarized()