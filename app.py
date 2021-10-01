from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route("/")
@app.route("/index")
def func_index():
    return "Welcome"


@app.route("/login")
def func_login():
    return render_template("login.html")


@app.route("/upload")
def func_upload():
    return render_template("upload.html")
