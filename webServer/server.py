import time
from subprocess import Popen, TimeoutExpired, PIPE
import os
import sys
import asyncio
from flask import Flask, render_template
from flask_socketio import SocketIO, send ,emit
import mysql.connector


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config["CACHE_TYPE"] = "null"

mydb = mysql.connector.connect(
  host="127.0.0.1",
  user="root",
  password="",
  database="drashti"
)

mycursor = mydb.cursor()

up = []
down = []


socketio = SocketIO(app, cors_allowed_origins="*")

def scanip(ip):
    cmd = "ping -c 1 " + ip + " -W 1000 > /dev/null"
    proc = Popen(cmd,stdout=PIPE,stderr=PIPE,shell=True)
    try:
        outs,errs = proc.communicate(timeout=1)
    except TimeoutExpired:
        proc.kill()
        return "0"
    if errs:
        return "0"
    return "1"

def runI():
    time.sleep(10)
    global up
    global down
    global mycursor
    newUp = []
    newDown = []

    mycursor.execute("SELECT ip FROM nodes")
    result = mycursor.fetchall()
    mycursor.close()
    mycursor = mydb.cursor() 
    result = [x[0] for x in result]
    print(result)
    for ip in result:
        if scanip(ip) == "1":
            newUp.append(ip)
        else:
            newDown.append(ip)
    print("✅",newUp)
    print("🚫",newDown)
    if(newUp != up or newDown != down):
        print("📲 Status is changed")
        emit('message','change',broadcast=True)

    up = newUp
    down = newDown

def checkServerStatus():
	print("Checking Server Status")

@socketio.on('message')
def handleMessage(msg):
     print("Message Received : ",msg)
     if msg == 'run':
         while True:
             runI()

@app.route('/',methods=['GET'])
def index():
	return render_template('index.html')


if __name__ == '__main__':
    socketio.run(app,port=4000)