from summarization.lexialRank import LexRankforSummarization

LexRank = LexRankforSummarization()

f = open("C:\\Users\\soicem\\Desktop\\robot_journalism\\summarization\\1.txt", 'r')
article1 = f.read()
if len(article1.strip().split('.')) > 3:
    summarizedArticles1 = LexRank.test_summarized(article1.replace('.', '.  '))
    print(summarizedArticles1)
f.close()

f = open("C:\\Users\\soicem\\Desktop\\robot_journalism\\summarization\\2.txt", 'r')
article2 = f.read()
tmp = article2.split('.')

summarizedArticles2 = LexRank.test_summarized(article2.replace('.', '.  ').strip())
print(summarizedArticles2)
f.close()

f = open("C:\\Users\\soicem\\Desktop\\robot_journalism\\summarization\\3.txt", 'r')
article3 = f.read()
if len(article3.split('.')) > 3:
    summarizedArticles3 = LexRank.test_summarized(article3.replace('.', '.  '))
    print(summarizedArticles3)
f.close()