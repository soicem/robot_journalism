# from cassandra.cluster import Cluster
# import time
#
#
# DROP TABLE IF EXISTS articles;
# create table articles (
#  	_id int not null auto_increment primary key,
#      tendency varchar(20) not null,
#      keyword varchar(20) not null,
#      title varchar(100),
#     target varchar(30) not null,
#     article TEXT,
#     articleUrl varchar(200) not null,
#     imgUrl varchar(200) not null,
#     publish_time datetime,
#     collecting_time datetime
# );
# DROP TABLE IF EXISTS summarizedArticles;
#  create table summarizedArticles (
#  	  _id int not null auto_increment primary key,
#      tendency varchar(20) not null,
#      keyword varchar(20) not null,
#      title varchar(100),
#      summurizedArticle TEXT,
#      imgUrl varchar(200) not null,
#      generatedtime datetime
#  );
# #키스페이스
# KEYSPACE = "robotjournalism"
#
# class mysqlDB:
#     def __init__(self):
#         self.conn = None
#         self.curs = None
#         self.datatimeFormat = "%04d-%02d-%02d %02d:%02d:%02d+0000"
#         self.session = None
#         self.mysql_init()
#
#     def mysql_init(self):
#         #카산드라 연결
#         cluster = Cluster(['127.0.0.1'])
#         self.session = cluster.connect()
#         #사용할 키스페이스 연결
#         self.session.set_keyspace(KEYSPACE)
#
#     def insertDataIntoArticles(self, tendency, keyword, title, target, article, articleUrl, published_time):
#         now = time.localtime()
#         collecting_time = self.datatimeFormat % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
#         # print(collecting_time)
#         title = title.lstrip().strip()
#         # title = title.lstrip()
#         # print("titledfdfs",title)
#         title = title.replace("'", '')
#         article = article.replace("'", '')
#         cql = "INSERT INTO articles (tendency, keyword, title, target, article, articleUrl, published_time, collecting_time) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s')"
#         cql = (cql % (tendency, keyword, title, target, article, articleUrl, published_time, collecting_time))
#         prepared = self.session.prepare(cql)
#         self.session.execute(prepared)
#
#     def insertDataIntoSummarizedArticles(self, tendency, keyword, title, summerizedArticle):
#         now = time.localtime()
#         title = title.lstrip()
#         s = self.datatimeFormat % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
#         cql = "INSERT INTO summarizedArticles (tendency, keyword, title, summarizedArticle, generatedtime) VALUES ('%s','%s','%s','%s', '%s')"
#         cql = (cql % (tendency, keyword, title, summerizedArticle, s))
#         prepared = self.session.prepare(cql)
#         self.session.execute(prepared)
#
#     def getTitleData(self, keyword, tendency):
#         now = time.gmtime() ## change timezone to gmt
#         if now.tm_hour-1<0:
#             conditionTime = self.datatimeFormat % (now.tm_year, now.tm_mon, now.tm_mday-1, 23, 59, 59)
#         else:
#             conditionTime = self.datatimeFormat % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour - 1, now.tm_min, now.tm_sec)
#         cql = "SELECT title FROM articles WHERE collecting_time >= '%s' and keyword = '%s' and tendency = '%s' ALLOW FILTERING;"
#         cql = (cql % (conditionTime, keyword, tendency))
#         # print(cql)
#         prepared = self.session.prepare(cql)
#         rows = self.session.execute(prepared)
#         return rows
#
#     def getArticleData(self, title):
#         cql = "select article from articles where title = '%s' ALLOW FILTERING"
#         cql = (cql % (title))
#         # print(cql)
#         prepared = self.session.prepare(cql)
#         rows = self.session.execute(prepared)
#         return rows
import pymysql
import time

class mysqlDB:
    def __init__(self):
        self.conn = None
        self.curs = None
        self.datatimeFormat = "%04d-%02d-%02d %02d:%02d:%02d"
        self.mysql_init()

    def mysql_init(self):
        # MySQL Connection 연결

        self.conn = pymysql.connect(host='localhost', user='root', passwd='1234', db='robotjournalism', charset='utf8')
        #robotjournalism

        # Connection 으로부터 Cursor 생성
        self.curs = self.conn.cursor()

    def mysql_close(self):
        self.curs.close()
        self.conn.close()

    # def insertDataIntoArticles(self, tendency, keyword, title, target, article, articleUrl, published_time):
    def insertDataIntoArticles(self, tendency, keyword, title, target, article, articleUrl,imgUrl, published_time):
        now = time.localtime()
        title = title.strip()
        s = self.datatimeFormat  % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
        sql = "insert into articles values(null,%s,%s,%s,%s,%s,%s,%s,%s,%s)" #위 sql문 오류나서

        self.curs.execute(sql,(tendency, keyword, title, target, article, articleUrl, imgUrl,published_time,s))
        self.conn.commit()

    def insertDataIntoSummarizedArticles(self, tendency, keyword, title,  summerizedArticle, imgUrl):
        now = time.localtime()
        s = self.datatimeFormat % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
        sql = "insert into summarizedArticles values(null,%s,%s,%s,%s,%s,%s)"
        self.curs.execute(sql,(tendency, keyword, title, summerizedArticle, imgUrl, s))
        self.conn.commit()

    def getSummarizedArticles(self,keywrod,tendency): #요약테이블내 데이터 1시간이내꺼 다불러옴
        now = time.localtime()
        conditionTime = self.datatimeFormat % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour - 1, now.tm_min, now.tm_sec)
        sql = "select summurizedArticle from summarizedArticles where keyword = %s and tendency=%s and generatedtime > %s; "
        self.curs.execute(sql,(keywrod,tendency,conditionTime))
        rows = self.curs.fetchall()
        SummarizedArticles_list=[]
        for row in rows:
            SummarizedArticles_list.append(row[0])
        return SummarizedArticles_list

    def getTitleData(self, keyword, tendency):
        now = time.localtime()

        if now.tm_hour-1 < 0 :
            conditionTime = self.datatimeFormat % (now.tm_year, now.tm_mon, now.tm_mday, 0,0,0)
        else:
            conditionTime = self.datatimeFormat % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour - 1, now.tm_min, now.tm_sec)

        print("conditionTime",conditionTime)
        sql = "select title from articles where keyword = %s and tendency=%s and collecting_time > %s;"
        self.curs.execute(sql, (keyword, tendency, conditionTime))
        rows = self.curs.fetchall()
        return rows

    def getArticleData(self, title):
        # sql = "select article from articles where title=%s"
        sql = "select article,imgUrl from articles where title=%s"
        self.curs.execute(sql, (title))
        rows = self.curs.fetchall()
        return rows

    # def getArticle_Image(self, title):
    #     sql = "select (article,imgUrl) from articles where title=%s"
    #     self.curs.execute(sql, (title))
    #     rows = self.curs.fetchall()
    #     return rows
    #
    # def getImgData(self, title):
    #     sql = "select imgUrl from articles where title=%s"
    #     self.curs.execute(sql, (title))
    #     rows = self.curs.fetchall()
    #     return rows