import time
from flask import Flask, request

app = Flask(__name__)


@app.route("/api/time")
def get_current_time():
    return {"time": time.time()}


@app.route("/api/account/verify_login")
def login_verify():
    return request.args["password"]
    return {"result": "1"}
