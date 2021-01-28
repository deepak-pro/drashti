from flask import Flask, render_template , redirect ,request , abort , request , jsonify
from flask_mail import Message , Mail
import mysql.connector
import os
from subprocess import Popen, TimeoutExpired, PIPE
import json

mydb = mysql.connector.connect(
  host="127.0.0.1",
  user="root",
  password="",
  database="drashti"
)

mycursor = mydb.cursor()

app = Flask(__name__)
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS = True,
    MAIL_USERNAME = 'drashtimonitoringtool@gmail.com',
    MAIL_PASSWORD = ''
)
mail = Mail(app)
mail.init_app(app)

@app.route('/')
def root():
    return redirect('/login',code=302)

@app.route('/waninfo')
def waninfo():
    return render_template('waninfo.html')

@app.route('/login', methods= ['GET','POST'])
def loginPage():
    if request.method == 'GET':
        return render_template("login.html")
    if request.method == 'POST':
        mycursor.execute("SELECT username,password FROM login")
        result = mycursor.fetchone()
        username,password = result
        user_username = request.form["username"]
        user_password = request.form["password"]

        if username == user_username and password == user_password:
            return redirect('/dashboard',code=302)
        else:
            return '<script>alert("Invalid login"); location.replace("/");</script>'
            

@app.route('/dashboard',methods=['GET'])
def dashboard():
    return render_template("dashboard.html")

@app.route('/notification',methods=['GET','POST'])
def notification():
    if request.method == 'GET':
        mycursor.execute("SELECT email FROM notification")
        emails = mycursor.fetchall()
        return render_template('notification.html',emails = emails)
    if request.method == 'POST':
        user_email = request.form["email"]
        query = "INSERT INTO notification values(%s)"
        mycursor.execute(query,[user_email])
        mydb.commit()
        return '<script>alert("Email Added successfully"); location.replace("/notification");</script>'

def sendMail(recipients,html):
    msg = Message("Hello",sender="drashtimonitoringtool@gmail.com",recipients=recipients)
    msg.html = html
    mail.send(msg)

@app.route('/testnotification',methods=['GET'])
def testNotification():
    mycursor.execute("SELECT email FROM notification")
    emails = mycursor.fetchall()
    recipients = [email[0] for email in emails ]
    html = "<h1>This is test notification</h1>"
    sendMail(recipients,html)
    return "Message Sent"

@app.route('/nodes',methods=['GET'])
def nodes():
    toReturn = []
    mycursor.execute("SELECT * FROM nodes")
    row_headers = [x[0] for x in mycursor.description]
    data = mycursor.fetchall()
    for result in data:
        toReturn.append(dict(zip(row_headers,result)))
    return jsonify(toReturn)

@app.route('/servers',methods=['GET'])
def servers():
    toReturn = []
    mycursor.execute("SELECT * FROM nodes where server=1")
    row_headers = [x[0] for x in mycursor.description]
    data = mycursor.fetchall()
    for result in data:
        toReturn.append(dict(zip(row_headers,result)))
    return jsonify(toReturn)
    

@app.route('/shownodes',methods=['GET'])
def shownodes():
    return render_template('shownodes.html')

@app.route('/showserver',methods=['GET'])
def showserverstatus():
    return render_template('showserver.html')

@app.route('/scannetwork',methods = ['GET'])
def scannetwork():
    return render_template('scannetwork.html')

@app.route('/scanip/<ip>',methods=['GET'])
def scanip(ip):
    cmd = "ping -c 1 " + ip + " -W 1000 > /dev/null"
    #return "1" if os.system(cmd) == 0 else "0"
    proc = Popen(cmd,stdout=PIPE,stderr=PIPE,shell=True)
    try:
        outs,errs = proc.communicate(timeout=1)
    except TimeoutExpired:
        print("🚫 " + ip + " is down")
        proc.kill()
        return "0"
    if errs:
        print("🚫there is an error")
        return "0"
    print("✅ " + ip + " is up")
    return "1"
    
@app.route('/addip/<ip>/<name>/<des>', methods=['GET'])
def addip(ip,name,des):
    query = 'INSERT INTO nodes (name,ip,description) values(%s,%s,%s)'
    try:
        mycursor.execute(query,[name,ip,des])
        mydb.commit()
    except:
        return "0"
    return "1"

@app.route('/addserver/<ip>',methods=['GET'])
def addserver(ip):
    query = 'UPDATE nodes set server=1 where ip=%s'
    try:
        mycursor.execute(query,[ip])
        print("✅ Added to Server")
        mydb.commit()
    except mysql.connector.Error as err:
        print("🚫",err)
        return "0"
    return "1"

@app.route('/removeserver/<ip>',methods=['GET'])
def removeserver(ip):
    query = 'UPDATE nodes set server=0 where ip=%s'
    try:
        mycursor.execute(query,[ip])
        print("✅ Removed ",ip," from server")
        mydb.commit()
    except mysql.connector.Error as err:
        print("🚫",err)
        return "0"
    return "1"

