#!/usr/bin/env python -W ignore::DeprecationWarning

import pymysql as mq
import time

while 1:
    print
    "db start"
    db = mq.connect("localhost", "pusan", "pusanpass", "pusandb")
    cursor = db.cursor()

    cursor.execute("select distinct id from sensor_table")
    ret = cursor.fetchall()
    for tup in list(ret):
        id = list(tup)[0]

        cursor.execute("select floor(avg(temperature)) from sensor_table where id=" + str(id))
        data = cursor.fetchone()

        cursor.execute("select temperature from sensor_table where id=" + str(id) + " order by time DESC limit 1 ")
        realData = cursor.fetchone()

        cursor.execute("select time from sensor_table where id=" + str(id) + " order by time DESC limit 1 ")
        date = cursor.fetchone()

        # print "insert into predictionVal values( 0, " + str(id) +", "+ str(int(result)) +" , '" + dateTime +"')"
        # cursor.execute(
        #     "insert into predictionVal values( 0, " + str(id) + ", " + str(int(result)) + " , '" + dateTime + "')")
        db.commit()

    time.sleep(5.00)
    print
    "server sleeping ..."
    db.close()
    print
    "db close"