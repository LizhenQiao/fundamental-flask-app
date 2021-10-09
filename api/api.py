import time
from flask import Flask, json, request, jsonify, session
from flask_mysqldb import MySQL
import yaml
from werkzeug.security import generate_password_hash, check_password_hash

# TODO: 基本功能完成后加try except， 暂时先删除了以免影响debug
app = Flask(__name__)
app.secret_key = "nothashfornow"

# configure db
db = yaml.load(open('static/db.yaml'), Loader=yaml.FullLoader)
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)


@app.route("/api/login", methods=['POST'])
def login():
    # Login logic. Only available for normal users. 
    try:
        data = request.get_json()
        username, password = data['username'], data['password']
        cur = mysql.connection.cursor()
        query = 'SELECT user_password FROM users WHERE user_name="{}"'.format(username)
        cur.execute(query)
        hashed_password = cur.fetchone()[0]
        if not hashed_password:
            raise Exception('No username matches.')
        cur.close()
        
        if check_password_hash(hashed_password, password):
            session['isLogin'] = 1
            return jsonify({"success": True})
    except Exception as e:
        print(e)
        return jsonify({"success": False, "error": ''})
        

@app.route("/api/admin_login", methods=['POST'])
def login():
    # Login logic. Only available for admin. 
    try:
        data = request.get_json()
        admin_username, admin_password = data['admin_username'], data['admin_password']
        cur = mysql.connection.cursor()
        query = 'SELECT admin_password FROM admins WHERE admin_name="{}"'.format(admin_username)
        cur.execute(query)
        password = cur.fetchone()[0]
        if not password:
            raise Exception('No username matches.')
        cur.close()
        
        if password == admin_password:
            session['isLogin'] = 1
            session['isAdmin'] = 1
            return jsonify({"success": True})
    except Exception as e:
        print(e)
        return jsonify({"success": False, "error": ''})


@app.route("/api/register", methods=['POST'])
def register():
    # Add new user accounts. Only available for admin.
    try:
        data = request.get_json()
        username, password = data['username'], data['password']
        hashed_password = generate_password_hash(password)
        cur = mysql.connection.cursor()
        query = 'INSERT INTO users(user_name, user_password) VALUES ("{}", "{}")'.format(username, hashed_password)
        cur.execute(query)
        mysql.connection.commit()
        cur.close()
        return jsonify({"success": True})
    except Exception as e:
        # TODO: 怎么在接口获取错误码
        print(e)
        return jsonify({"success": False, "error": ''})


@app.route("/api/delete_account", methods=['POST'])
def deleteAccount():
    # Delete user accounts. Only available for admin.
    data = request.get_json()
    # TODO: 删除账号之后前端做成可视化操作的状态，不过不影响接口后端代码
    pass


@app.route("/api/upload", methods=['POST'])
def upload():
    # upload files. Only available for normal users.
    data = request.get_json()

    return jsonify({"result": "success", "data": data})


@app.route("/api/changePassword", methods=['POST'])
def changePassword():
    # change password.
    data = request.get_json()

    return jsonify({"result": "success"})


@app.route("/api/photos", methods=['POST'])
def get_photos():
    # get all the photos of certain user. 
    data = request.get_json()

    return jsonify({"result": "success"})
