#!/usr/bin/env python -W ignore::DeprecationWarning

# - MySQL robotjournalism database table query
# use robotjournalism;
#
# DROP TABLE IF EXISTS articles;
#
# create table articles (
# 	_id int not null auto_increment primary key,
#     tendency varchar(20) not null,
#     keyword varchar(20) not null,
#     title varchar(100),
#     target varchar(30) not null,
#     article TEXT,
#     articleUrl varchar(200) not null,
#     publish_time datetime,
#     collecting_time datetime
# );
#
#
# use robotjournalism;
#
# DROP TABLE IF EXISTS summarizedArticles;
#
# create table summarizedArticles (
# 	  _id int not null auto_increment primary key,
#     tendency varchar(20) not null,
#     keyword varchar(20) not null,
#     summurizedArticle TEXT,
#     generatedtime datetime
# );
#
#
# use robotjournalism;
#
# DROP TABLE IF EXISTS errorLogTable;
#
# create table errorLogTable (
# 	  _id int not null auto_increment primary key,
#     errorCategorize varchar(20) not null,
#     errorType varchar(20) not null,
#     occuredtime datetime
# );

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
        # self.conn = pymysql.connect(host='localhost', user='root', password='1234',
        #                         db='robotjournalism', charset='utf8')

        self.conn = pymysql.connect(host='localhost', user='root', passwd='1234', db='robotjournalism', charset='utf8')
        #robotjournalism

        # Connection 으로부터 Cursor 생성
        self.curs = self.conn.cursor()

    def mysql_close(self):
        self.curs.close()
        self.conn.close()

    def insertDataIntoArticles(self, tendency, keyword, title, target, article, articleUrl, published_time):
        now = time.localtime()
        s = self.datatimeFormat  % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)

        sql = "insert into articles values(null,%s,%s,%s,%s,%s,%s,%s,%s)" #위 sql문 오류나서
        self.curs.execute(sql,(tendency, keyword, title, target, article, articleUrl, published_time,s))
        self.conn.commit()

    def insertDataIntoSummarizedArticles(self, tendency, keyword, summerizedArticle):
        now = time.localtime()
        s = self.datatimeFormat % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)

        sql = "insert into summarizedArticles values(null,%s,%s,%s,%s);"
        self.curs.execute(sql,(tendency, keyword, summerizedArticle, s))
        self.conn.commit()

    # def getAllData(self):
    #     sql = "select article from articles where _id=1; "
    #     self.curs.execute(sql)
    #     rows = self.curs.fetchall()
    #     return rows

    def getTitleData(self, keyword, tendency):
        now = time.localtime()
        conditionTime = self.datatimeFormat % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour - 1, now.tm_min, now.tm_sec)
        sql = "select title from articles where keyword = %s and tendency=%s and collecting_time > %s;"
        self.curs.execute(sql, (keyword, tendency, conditionTime))
        rows = self.curs.fetchall()
        return rows

    def getArticleData(self, title):
        sql = "select article from articles where title=%s;"
        self.curs.execute(sql, (title))
        rows = self.curs.fetchall()
        return rows



