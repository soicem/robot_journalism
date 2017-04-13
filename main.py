import Article

if __name__=="__main__":
    # tendency = input("tendency : ")
    # keyword = input("keyword : ")
    keyword='안철수'
    ar = Article.Article("progressivism", keyword)
    # ar = Article.Article(tendency, keyword)
    ar.gathering()
