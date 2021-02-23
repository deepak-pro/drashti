from flask import Flask, render_template , redirect ,request , abort , request , jsonify
from flask_mail import Message , Mail
import mysql.connector
import os
from subprocess import Popen, TimeoutExpired, PIPE
import json

#mydb = mysql.connector.connect(host="127.0.0.1",user="root",password="",database="drashti")
#mycursor = mydb.cursor()

app = Flask(__name__)
app.config["CACHE_TYPE"] = "null"
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS = True,
    MAIL_USERNAME = 'drashtimonitoringtool@gmail.com',
    MAIL_PASSWORD = 'testPassword'
)
mail = Mail(app)
mail.init_app(app)

@app.route('/')
def root():
    return redirect('/login',code=302)

@app.route('/waninfo')
def waninfo():
    return render_template('waninfon.html',titlepath="Wan Info")

def loguser(username):
    mydb = mysql.connector.connect(host="127.0.0.1",user="root",password="",database="drashti")
    mycursor = mydb.cursor()

    query = "INSERT INTO logs (username) values(%s)"
    mycursor.execute(query,[username])
    mydb.commit()

    mydb.close()

@app.route('/login', methods= ['GET','POST'])
def loginPage():
    mydb = mysql.connector.connect(host="127.0.0.1",user="root",password="",database="drashti")
    mycursor = mydb.cursor()
    if request.method == 'GET':
        return render_template("loginn.html")
    if request.method == 'POST':
        mycursor.execute("SELECT username,password FROM login")
        result = mycursor.fetchone()
        username,password = result
        user_username = request.form["username"]
        user_password = request.form["password"]

        if username == user_username and password == user_password:
            loguser(username)
            return redirect('/dashboard',code=302)
        else:
            return '<script>alert("Invalid login"); location.replace("/");</script>'
    mydb.close()
            

@app.route('/dashboard',methods=['GET'])
def dashboard():
    return render_template("dashboardn.html",titlepath="Dashboard")

@app.route('/notification',methods=['GET','POST'])
def notification():
    mydb = mysql.connector.connect(host="127.0.0.1",user="root",password="",database="drashti")
    mycursor = mydb.cursor()
    if request.method == 'GET':
        mycursor.execute("SELECT email FROM notification")
        emails = mycursor.fetchall()
        mydb.close()
        return render_template('notificationn.html',emails = emails,titlepath="Wan Info")
    if request.method == 'POST':
        user_email = request.form["email"]
        query = "INSERT INTO notification values(%s)"
        mycursor.execute(query,[user_email])
        mydb.commit()
        mydb.close()
        return '<script>alert("Email Added successfully"); location.replace("/notification");</script>'

def sendMail(recipients,html):
    msg = Message("Hello",sender="drashtimonitoringtool@gmail.com",recipients=recipients)
    msg.html = html
    mail.send(msg)

@app.route('/testnotification',methods=['GET'])
def testNotification():
    print("Sending email for testing notification")
    mydb = mysql.connector.connect(host="127.0.0.1",user="root",password="",database="drashti")
    mycursor = mydb.cursor()
    mycursor.execute("SELECT email FROM notification")
    emails = mycursor.fetchall()
    mydb.close()
    recipients = [email[0] for email in emails ]
    html = "<h1>This is test notification</h1>"
    sendMail(recipients,html)
    return "Message Sent"

@app.route('/nodes',methods=['GET'])
def nodes():
    toReturn = []
    mydb = mysql.connector.connect(host="127.0.0.1",user="root",password="",database="drashti")
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM nodes")
    row_headers = [x[0] for x in mycursor.description]
    data = mycursor.fetchall()
    mydb.close()
    for result in data:
        toReturn.append(dict(zip(row_headers,result)))
    return jsonify(toReturn)

@app.route('/servers',methods=['GET'])
def servers():
    mydb = mysql.connector.connect(host="127.0.0.1",user="root",password="",database="drashti")
    mycursor = mydb.cursor()
    toReturn = []
    mycursor.execute("SELECT * FROM nodes where server=1")
    row_headers = [x[0] for x in mycursor.description]
    data = mycursor.fetchall()
    mydb.close()
    for result in data:
        toReturn.append(dict(zip(row_headers,result)))
    return jsonify(toReturn)


@app.route("/getnodes")
def getnodes():
    toReturn = ""
    mydb = mysql.connector.connect(host="127.0.0.1",user="root",password="",database="drashti")
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM nodes")
    data = mycursor.fetchall()
    mydb.close()
    for result in data:
        toReturn = toReturn + ";" + result[0]
    return str(toReturn)

@app.route('/stats')
def stats():
    toReturn = ""

    mydb = mysql.connector.connect(host="127.0.0.1",user="root",password="",database="drashti")
    mycursor = mydb.cursor()
    mycursor.execute("SELECT COUNT(*) FROM nodes")
    totalNodes = mycursor.fetchall()[0][0]
    mydb.close()

    mydb = mysql.connector.connect(host="127.0.0.1",user="root",password="",database="drashti")
    mycursor = mydb.cursor()
    mycursor.execute("SELECT COUNT(*) FROM nodes where server=1")
    totalServers = mycursor.fetchall()[0][0]
    mydb.close()

    mydb = mysql.connector.connect(host="127.0.0.1",user="root",password="",database="drashti")
    mycursor = mydb.cursor()
    mycursor.execute('SELECT COUNT(*) FROM nodes where server="1" and status="1"')
    activeServers = mycursor.fetchall()[0][0]
    mydb.close()

    mydb = mysql.connector.connect(host="127.0.0.1",user="root",password="",database="drashti")
    mycursor = mydb.cursor()
    mycursor.execute('SELECT COUNT(*) FROM nodes where server="1" and status="0"')
    inactiveServer = mycursor.fetchall()[0][0]
    mydb.close()

    toReturn = str(totalNodes) + " " + str(totalServers) + " " + str(activeServers) + " " + str(inactiveServer)
    return str(toReturn)
    

@app.route('/shownodes',methods=['GET'])
def shownodes():
    return render_template('shownodesn.html',titlepath="Nodes")

@app.route('/faq',methods=['GET'])
def faq():
    return render_template('faq.html',titlepath="FAQ")

@app.route('/showlogs',methods=['GET'])
def showlogs():
    mydb = mysql.connector.connect(host="127.0.0.1",user="root",password="",database="drashti")
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM logs")
    logs = mycursor.fetchall()
    mydb.close()
    return render_template('showlogsn.html',titlepath="Logs",logs=logs)

@app.route('/showserver',methods=['GET'])
def showserverstatus():
    return render_template('showservern.html',titlepath="Servers")

@app.route('/scannetwork',methods = ['GET'])
def scannetwork():
    return render_template('scannetworkn.html',titlepath="Scan Network")

@app.route('/scanip/<ip>',methods=['GET'])
def scanip(ip):
    cmd = "ping -c 1 " + ip + " -W 1000 > /dev/null"
    #return "1" if os.system(cmd) == 0 else "0"
    proc = Popen(cmd,stdout=PIPE,stderr=PIPE,shell=True)
    try:
        outs,errs = proc.communicate(timeout=1)
    except TimeoutExpired:
        #print("🚫 " + ip + " is down")
        proc.kill()
        return "0"
    if errs:
        print("🚫there is an error")
        return "0"
    #print("✅ " + ip + " is up")
    return "1"
    
@app.route('/addip/<ip>/<name>/<des>', methods=['GET'])
def addip(ip,name,des):
    mydb = mysql.connector.connect(host="127.0.0.1",user="root",password="",database="drashti")
    mycursor = mydb.cursor()
    query = 'INSERT INTO nodes (name,ip,description) values(%s,%s,%s)'
    try:
        mycursor.execute(query,[name,ip,des])
        mydb.commit()
        mydb.close()
    except:
        mydb.close()
        return "0"
    return "1"

@app.route('/addserver/<ip>',methods=['GET'])
def addserver(ip):
    mydb = mysql.connector.connect(host="127.0.0.1",user="root",password="",database="drashti")
    mycursor = mydb.cursor()
    query = 'UPDATE nodes set server=1 where ip=%s'
    try:
        mycursor.execute(query,[ip])
        #print("✅ Added to Server")
        mydb.commit()
        mydb.close()
    except mysql.connector.Error as err:
        #print("🚫",err)
        return "0"
        mydb.close()
    return "1"

@app.route('/removeserver/<ip>',methods=['GET'])
def removeserver(ip):
    mydb = mysql.connector.connect(host="127.0.0.1",user="root",password="",database="drashti")
    mycursor = mydb.cursor()
    query = 'UPDATE nodes set server=0 where ip=%s'
    try:
        mycursor.execute(query,[ip])
        #print("✅ Removed ",ip," from server")
        mydb.commit()
        mydb.close()
    except mysql.connector.Error as err:
        print("🚫",err)
        mydb.close()
        return "0"
    return "1"

@app.route('/removenode/<ip>',methods=['GET'])
def removenode(ip):
    mydb = mysql.connector.connect(host="127.0.0.1",user="root",password="",database="drashti")
    mycursor = mydb.cursor()
    query = "DELETE FROM nodes WHERE ip=%s"
    try:
        mycursor.execute(query,[ip])
        mydb.commit()
        mydb.close()
    except mysql.connector.Error as err:
        print("Error ", err)
        return "0"
    return "1"

