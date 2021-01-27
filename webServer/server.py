import time
from subprocess import Popen, TimeoutExpired, PIPE
import os
import sys
import asyncio
from flask import Flask, render_template
from flask_socketio import SocketIO, send ,emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config["CACHE_TYPE"] = "null"

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
    up = []
    down = []
    for i in range(11):
        if scanip('192.168.1.'+str(i)) == "1":
            up.append('192.168.1.'+str(i))
        else:
            down.append('192.168.1.'+str(i))
    print("✅",up)
    print("🚫",down)
    emit('message','up and down')

def checkServerStatus():
	print("Checking Server Status")

@socketio.on('message')
def handleMessage(msg):
     print("Message Received : ",msg)
     if msg == 'run':
         runI()

@app.route('/',methods=['GET'])
def index():
	return render_template('index.html')


if __name__ == '__main__':
	socketio.run(app,port=4000)