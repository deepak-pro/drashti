from flask import Flask, render_template , redirect ,request
from flask_mail import Message , Mail
import mysql.connector
import os

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

@app.route('/scannetwork',methods = ['GET'])
def scannetwork():
    return render_template('scannetwork.html')

@app.route('/scanip/<ip>',methods=['GET'])
def scanip(ip):
    return "1" if os.system("ping -c 1 " + ip + " -W 1000 > /dev/null" ) == 0 else "0"
    
@app.route('/addip/<ip>/<name>', methods=['GET'])
def addip(ip,name):
    query = 'INSERT INTO nodes values(%s,%s)'
    try:
        mycursor.execute(query,[name,ip])
        mydb.commit()
    except:
        return "0"
    return "1"