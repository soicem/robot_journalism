#!/usr/bin/env python -W ignore::DeprecationWarning

# - MySQL robotjournarism database table query
# use robotjournalism;
#
# DROP TABLE IF EXISTS articles;
#
# create table articles (
# 	_id int not null auto_increment primary key,
#     tendency int not null,
#     title varchar(30),
#     target varchar(30) not null,
#     article TEXT,
#     articleUrl varchar(50) not null,
#     publish_time datetime,
#     collecting_time datetime
# );
#
# insert into articles values(null , 1, "쿵짝쿵짝 도천 천곡", "한겨례", "best in the world", "knq1130@naver.com","9999-12-31 23:59:59", "9999-12-31 23:59:59");
# select * from articles;

import pymysql
import time

class mysqlDB:
    def __init__(self):
        self.conn = None
        self.curs = None
        self.mysql_init()

    def mysql_init(self):
        # MySQL Connection 연결
        self.conn = pymysql.connect(host='localhost', user='root', password='1234',
                               db='robotjournalism', charset='utf8')
        # Connection 으로부터 Cursor 생성
        self.curs = self.conn.cursor()

    def mysql_close(self):
        self.curs.close()
        self.conn.close()

    def insert_data(self, tendency, title, target, article, articleUrl, published_time):
        now = time.localtime()
        s = "%04d-%02d-%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
        print(title)
        sql = "insert into articles values(null , "+ \
              tendency +',' \
              '"' + title + '",' + \
              '"' + target + '",' + \
              '"' + article +'",' + \
              '"' + articleUrl +'",' + \
              '"' + published_time + '",' + \
              '"' + s + '");'
        # print(sql)
        self.curs.execute(sql)
        self.conn.commit()

    def printData(self):
        sql = "select * from articles"
        self.curs.execute(sql)
        rows = self.curs.fetchall()
        for row in rows:
            print(row)



