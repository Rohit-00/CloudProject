import MySQLdb
from flask import Flask, redirect, render_template,request, session, url_for
from datetime import datetime
from flask_mysqldb import MySQL
import mysql.connector

from bs4 import BeautifulSoup
app = Flask(__name__)

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='school'

mysql= MySQL(app)
app.secret_key='SecretKey'



# Main app (login)
@app.route("/", methods=['GET','POST'])
def login():
    msg=''
    
    if request.method == 'POST':
        username=request.form['user']
        password=request.form['pass']

        cur = mysql.connection.cursor()
        sql="Select *from admins where username = %s and pass = %s"
        args = [username,password,]
        cur.execute(sql,args)
        record = cur.fetchone()
        mysql.connection.commit()
        cur.close()
        if record:
            session['loggedin']=True
            session['username']=record[1]
            cur.execute
            return redirect(url_for('hello_world'))

        else:
            msg='Incorrect username/passowrd'
        
    return render_template("auth.html",msg=msg)





@app.route('/compile', methods=['POST'])
def compile():
    code = request.form['code']
    soup = BeautifulSoup(code, 'html.parser')
    return soup.prettify()



# Landing page
@app.route("/main")
def hello_world(): 
    return render_template('index.html')


# app for inserting into student table
@app.route("/insert", methods=[ 'GET','POST'])
def insert():
    if request.method=='POST':
        sid = request.form['sid']
        rollno=request.form['rollno']
        fname=request.form['fname']
        lname=request.form['lname']
        std=request.form['class']
        phone=request.form['phone']
        address=request.form['address']


    
        cur = mysql.connection.cursor()
        sql="INSERT INTO students(sid,rollno,fname,lname,class,phone,address)" "VALUES (%s,%s,%s,%s,%s,%s,%s)"
        args = [sid,rollno,fname,lname,std,phone,address,]
        cur.execute(sql,args)
        mysql.connection.commit()
        
        
        return render_template("index.html")
    
    return render_template("index.html")


# app to insert into teachers table
@app.route("/insertteachers", methods=['GET', 'POST'])
def insertteachers():
    if request.method=='POST':
        tid = request.form['id']
        name=request.form['name']
        phone=request.form['phone']
        email=request.form['email']
        address=request.form['address']
        age=request.form['age']
        doj=request.form['doj']
        term=request.form['term']
        design=request.form['design']
        std=request.form['class']
        gender=request.form['gender']

    
        cur = mysql.connection.cursor()
        sql="INSERT INTO teachers(tid,tname,phone,email,city,age,doj,term,designation,class,experience)" "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        args = [tid,name,phone,email,address,age,doj,term,design,std,gender,]
        cur.execute(sql,args)
        mysql.connection.commit()
        
        return render_template("addteach.html")
  
    return render_template("addteach.html")


# app to update students data
@app.route('/updatestudent/<id>/',methods=['GET','POST'])
def updatestudent(id):
    if request.method=='POST':
        sid = request.form['sid']
        rollno=request.form['rollno']
        fname=request.form['fname']
        lname=request.form['lname']
        std=request.form['class']
        phone=request.form['phone']
        address=request.form['address']
        
    
        cur=mysql.connection.cursor()
        cur.execute("update students set sid= %s, rollno = %s, fname= %s, lname=%s, class=%s,phone=%s,address=%s where sid = %s",[sid,rollno,fname,lname,std,phone,address,id])
        mysql.connection.commit() 

    cur = mysql.connection.cursor()

    mysql.connection.commit()
    cur.execute("SELECT * FROM students where sid=%s",[id,])
    rows = cur.fetchone()
    cur.close() 
    return render_template('updatestudent.html',rows=rows)


# app to update teachers data
@app.route('/updateteach/<id>/',methods=['GET','POST'])
def updateteach(id):
    if request.method=='POST':
        tid = request.form['id']
        name=request.form['name']
        phone=request.form['phone']
        email=request.form['email']
        address=request.form['address']
        age=request.form['age']
        doj=request.form['doj']
        term=request.form['term']
        design=request.form['design']
        std=request.form['class']
        gender=request.form['gender']
    
        cur=mysql.connection.cursor()
        cur.execute("update teachers set tid = %s ,tname = %s,phone = %s,email = %s,city = %s,age = %s,doj =%s,term =%s,designation = %s,class = %s,experience = %s where tid = %s ",[tid,name,phone,email,address,age,doj,term,design,std,gender,id])
        mysql.connection.commit() 

    cur = mysql.connection.cursor()

    mysql.connection.commit()
    cur.execute("SELECT * FROM teachers where tid=%s",[id,])
    rows = cur.fetchone()
    cur.close() 
    return render_template('updateteach.html',rows=rows)


# app to delete students data
@app.route('/delete/<id>/',methods=['GET','POST'])
def delete(id):
        cursor=mysql.connection.cursor()
        cursor.execute("DELETE FROM result WHERE sid = %s",(id,),)
        mysql.connection.commit()
        cursor.execute("DELETE FROM students WHERE sid = %s",(id,),)
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('view'))

# app to delete teachers data
@app.route('/deleteteach/<id>/',methods=['GET','POST'])
def deleteteach(id):
        cursor=mysql.connection.cursor()
        
        cursor.execute("DELETE FROM teachers WHERE tid = %s",(id,),)
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('viewteach'))

# app to view students data
@app.route('/view',methods=['GET'])
def view():
        cur = mysql.connection.cursor()
        
        cur.execute("SELECT * FROM students")
        mysql.connection.commit()
        rows = cur.fetchall()
        cur.close()
        
        return render_template("viewstudent.html",rows=rows)
    
# app to view teachers data
@app.route('/viewteach',methods=['GET'])
def viewteach():
        cur = mysql.connection.cursor()
        
        cur.execute("SELECT * FROM teachers")
        mysql.connection.commit()
        rows = cur.fetchall()
        cur.close()
        
        return render_template("viewteach.html",rows=rows)   

# app to add result
@app.route('/result/<id>',methods=['GET','POST'])
def result(id):
    if request.method=='POST':
        sid = request.form['id']
        name=request.form['name']
        sub1=request.form['sub1']
        sub2=request.form['sub2']
        sub3=request.form['sub3']
        sub4=request.form['sub4']
        sub5=request.form['sub5']
        total=request.form['txtf']
        percentage=request.form['txtg']
       

        cur=mysql.connection.cursor()
        cur.execute("INSERT INTO result(sid,name,sub1,sub2,sub3,sub4,sub5,total,percentage)" "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",[sid,name,sub1,sub2,sub3,sub4,sub5,total,percentage])
        mysql.connection.commit() 

        
        
    cur = mysql.connection.cursor()

    mysql.connection.commit()
    cur.execute("SELECT * FROM students where sid=%s",[id,])
    rows = cur.fetchone()
    cur.close()     
    return render_template('result.html',rows=rows)

# app to view result
@app.route('/viewresult/<id>',methods=['GET'])
def viewresult(id):

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM result where sid = %s",[id,])
        mysql.connection.commit()
        rows = cur.fetchone()
        cur.close()
        
        return render_template("viewresult.html",rows=rows)   
    
if __name__ == "__main__":
    app.run(debug=True,port=8000)
