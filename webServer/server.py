import os
import time
import smtplib
import mysql.connector
from flask_mail import Message , Mail
from subprocess import Popen, TimeoutExpired, PIPE

up = []
down = []

def sendEmail(ip,name):
    print("Sending email for ip ",ip," and name ",name)
    mydb = mysql.connector.connect(host="127.0.0.1",user="root",password="",database="drashti")
    mycursor = mydb.cursor()

    mycursor.execute("SELECT email FROM notification")
    data = mycursor.fetchall()
    mycursor.close()
    mycursor = mydb.cursor()
    mydb.close()

    emails = [email[0] for email in data]
    gmail_user = 'drashtimonitoringtool@gmail.com'
    gmail_password = 'testPassword'

    sent_from = gmail_user
    to = emails
    subject = name + ' is Down'
    body = 'You machine : ' + name + " with ip " + ip + " just went down."

    email_text = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (sent_from, ", ".join(to), subject, body)

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to, email_text)
        server.close()
        print('Email sent!')
    except:
        print('Something went wrong...')



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

def changeStatus(status,ip):
    mydb = mysql.connector.connect(host="127.0.0.1",user="root",password="",database="drashti")
    mycursor = mydb.cursor()

    query = 'UPDATE nodes set status=%s where ip=%s'
    try:
        mycursor.execute(query,[status,ip])
    except:
        print("Error updating data.")
    print("Record updated")

    mydb.commit()
    mydb.close()

def runI():
    time.sleep(1)

    global up
    global down

    newUp = []
    newDown = []

    mydb = mysql.connector.connect(host="127.0.0.1",user="root",password="",database="drashti")
    mycursor = mydb.cursor()

    mycursor.execute("SELECT ip FROM nodes")
    data = mycursor.fetchall()
    mycursor.close()
    mycursor = mydb.cursor()
    mydb.close()

    result = [x[0] for x in data]
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
        if newUpIps:
            for ip in newUpIps:
                changeStatus(1,ip)
        if newDownIps:
            for ip in newDownIps:
                changeStatus(0,ip)
                mydb = mysql.connector.connect(host="127.0.0.1",user="root",password="",database="drashti")
                mycursor = mydb.cursor()
                mycursor.execute("SELECT ip,name FROM nodes WHERE server=1 AND status=0")
                downServers = mycursor.fetchall()
                mycursor.close()
                mycursor = mydb.cursor()
                mydb.close()

                for record in list(downServers):
                    if record[0] in newDownIps:
                        sendEmail(record[0],record[1])


    up = newUp
    down = newDown


if __name__ == '__main__':
    print("Running Program...")
    while True:
        runI()