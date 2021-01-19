from flask import Flask, render_template , redirect ,request

app = Flask(__name__)

@app.route('/')
def root():
    return redirect('/login',code=302)

@app.route('/login', methods= ['GET','POST'])
def loginPage():
    if request.method == 'GET':
        return render_template("login.html")
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        if username == "d" and password == "j":
            return redirect('/dashboard',code=302)
        else:
            return '<script>alert("Invalid login"); location.replace("/");</script>'
            

@app.route('/dashboard',methods=['GET'])
def dashboard():
    return "Dashboard"
