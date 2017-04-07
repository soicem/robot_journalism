#!/usr/bin/env python -W ignore::DeprecationWarning

# - MySQL robotjournarism database table query
# use robotjournalism;
#
# DROP TABLE IF EXISTS articles;
#
# create table articles (
# 	_id int not null auto_increment primary key,
#     tendency int not null,
#     target varchar(30) not null,
#     article TEXT,
#     articleUrl varchar(50) not null,
#     publish_time datetime,
#     collecting_time datetime
# );
#
# insert into articles values(null , 1, "한겨례", "best in the world", "knq1130@naver.com",
# "9999-12-31 23:59:59", "9999-12-31 23:59:59");
# select * from articles;

import pymysql

# MySQL Connection 연결
conn = pymysql.connect(host='localhost', user='root', password='1234',
                       db='robotjournalism', charset='utf8')

# Connection 으로부터 Cursor 생성
curs = conn.cursor()

sql = "select * from articles"
curs.execute(sql)

rows = curs.fetchall()
print(rows)  # 전체 rows
