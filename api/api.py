import time
from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
import yaml

app = Flask(__name__)

# configure db
db = yaml.load(open('./static/db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)


@app.route("/api/time")
def get_current_time():
    return {"time": time.time()}


@app.route("/api/login", methods=['POST'])
def login():
    data = request.get_json()

    cur = mysql.connection.cursor()
    query = "SELECT password FROM accounts WHERE username='{}'".format(data['username'])
    cur.execute(query)
    mysql.connection.commit()
    cur.close()
    return jsonify({"success": True})


@app.route("/api/register", methods=['POST'])
def register():
    try:
        data = request.get_json()

        cur = mysql.connection.cursor()

        query = "INSERT INTO Accounts(username, password) VALUES('{}', '{}');".format(data['username'], data['password'])
        cur.execute(query)
        mysql.connection.commit()
        cur.close()
        return jsonify({"success": True, "data": data})
    except:
        # TODO: 怎么在接口获取错误码
        return jsonify({"success": False, "error": {}})


@app.route("/api/delete_account", methods=['POST'])
def deleteAccount():
    data = request.get_json()


@app.route("/api/upload", methods=['POST'])
def upload():
    data = request.get_json()

    return jsonify({"result": "success", "data": data})


@app.route("/api/changePassword", methods=['POST'])
def changePassword():
    data = request.get_json()

    return jsonify({"result": "success"})

@app.route("/api/photos", methods=['POST'])
def get_photos():
    data = request.get_json()

    return jsonify({"result": "success"})
