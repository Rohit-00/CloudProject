#run only one time to create database

import mysql.connector




mysql.connector.connect(user='root', password='', host='localhost', database='school')

cur = mysql.connection.cursor()

cur.execute("Create database school")
cur.execute("Use school")
cur.execute("create table students(sid integer primary key,rollno integer,fname varchar(20),lname varchar(20),class varchar(20),phone integer,address varchar(20)")
cur.execute("create table result(sid foriegn key references students(sid),name varchar(20), sub1 integer, sub2 integer, sub3 integer, sub4 integer, sub5 integer, total integer, percentage integer)")
cur.execute("create table teachers(tid integer primary key, tname varchar(20),phone integer,email varchar(20),city varchar(20),age integer,doj date,term varchar(20),designation varchar(20),class varchar(10), experience varchar(20)")

mysql.connection.commit()
cur.close()







