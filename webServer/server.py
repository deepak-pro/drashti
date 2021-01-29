import time
import os
import mysql.connector
from subprocess import Popen, TimeoutExpired, PIPE

up = []
down = []

def scanip(ip):
    cmd = "ping -c 1 " + ip + " -W 1000 > /dev/null"
    proc = Popen(cmd,stdout=PIPE,stderr=PIPE,shell=True)
    try:
        _,errs = proc.communicate(timeout=1)
    except TimeoutExpired:
        proc.kill()
        return "0"
    if errs:
        return "0"
    return "1"

def changeStatus(ip,status):
    mydb = mysql.connector.connect(host="127.0.0.1",user="root",password="",database="drashti")
    mycursor = mydb.cursor()

    query = 'UPDATE nodes set server=%s where ip=%s'
    try:
        mycursor.execute(query,[status,ip])
    except:
        print("Error updating data.")
    print("Record updated")

    mydb.commit()
    mydb.close()

def runI():
    time.sleep(2)

    global up
    global down

    newUp = []
    newDown = []

    mydb = mysql.connector.connect(host="127.0.0.1",user="root",password="",database="drashti")
    mycursor = mydb.cursor()

    mycursor.execute("SELECT ip FROM nodes")
    result = mycursor.fetchall()
    mycursor.close()
    mycursor = mydb.cursor()
    mydb.close()

    result = [x[0] for x in result]
    print("Checking ",result)
    for ip in result:
        if scanip(ip) == "1":
            newUp.append(ip)
        else:
            newDown.append(ip)
    
    print("✅",newUp)
    print("🚫",newDown)

    if(newUp != up or newDown != down):
        print("📲 Status is changed")
        newUpIps = [ip for ip in newUp if ip not in up]
        newDownIps = [ip for ip in newDown if ip not in down]
        print("New up ip are ", newUpIps)
        print("New down ip are ",newDownIps)

    up = newUp
    down = newDown


if __name__ == '__main__':
    print("Running Program...")
    while True:
        runI()