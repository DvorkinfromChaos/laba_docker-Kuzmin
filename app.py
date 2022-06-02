import time
import redis
from flask import Flask
import pymysql
import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)


@app.route('/')
def web():
    #redis
    count = get_hit_count()
    #-------------------------------
    #sql
    connection = pymysql.connect(
    host='mysql',
    user='user',
    password='test',
    database='myDb',
    cursorclass=pymysql.cursors.DictCursor)
    with connection.cursor() as cursor:
        try:
            create_table_query = "CREATE TABLE `laba`(id int AUTO_INCREMENT," \
                                " name varchar(32)," \
                                " password varchar(32), PRIMARY KEY (id));"
            cursor.execute(create_table_query)
        except:
            pass
    with connection.cursor() as cursor:
        insert_query = "INSERT INTO `laba` (name, password) VALUE ('ono rabotaet', 'rabotaet je');"
        cursor.execute(insert_query)
        connection.commit()
        
    with connection.cursor() as cursor:
        select_all_rows = "SELECT * FROM `laba`"
        cursor.execute(select_all_rows)
        rows = cursor.fetchall()
        result = ''
        for row in rows:
            result += str(row) + '<br>'
    #--------------------------------
    #PostgreSQL
    con = psycopg2.connect(
    host = "postgress_sql",
    database = 'myDb',
    user = "user",
    password = "test") 
    con.autocommit = True
    with con.cursor() as cursor:
        try:    
            create_table_query = """CREATE TABLE labapost(
                                    id serial PRIMARY KEY,
                                    name varchar(32) NOT NULL,
                                    password varchar(32) NOT NULL);"""
            cursor.execute(create_table_query)
        except:
            pass
    with con.cursor() as cursor:
        cursor.execute(
            """INSERT INTO labapost (name, password) VALUES
            ('OCHEN', 'OCHEN');"""
        )
    with con.cursor() as cursor:
        select_all_rows = "SELECT * FROM labapost"
        cursor.execute(select_all_rows)
        rows = cursor.fetchall()
        result1 = ''
        for row in rows:
            result1 += str(row) + '<br>'  
    #--------------------------------
    outcome = '\nHello World Docker! I have been seen {} times.\n\n'.format(count)+ "<br>DB sql:<br>" + result + "<br>DB PostgreSQL :<br>" + result1
    return outcome