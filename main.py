from robot_journalism import Article

if __name__=="__main__":
    tendency = input("tendency : ")
    keyword = input("keyword : ")
    ar = Article.Article(tendency, keyword)
    ar.gathering()
