from flask import Flask, render_template , redirect ,request
import mysql.connector

mydb = mysql.connector.connect(
  host="172.16.72.3",
  user="deepak",
  password="forth",
  database="drashti"
)

mycursor = mydb.cursor()

app = Flask(__name__)

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

@app.route('/testnotification',methods=['GET'])
def testNotification():
    return "Testing notification"