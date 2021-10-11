from flask import Flask, json, request, jsonify, session
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
from wand.image import Image
from urllib.parse import urlparse
from werkzeug.utils import secure_filename
import yaml
import os
import validators


# TODO: 基本功能完成后加try except， 暂时先删除了以免影响debug
app = Flask(__name__)
app.secret_key = "nothashfornow"
CORS(app)

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'bmp'])
BASEDIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_UPLOAD = os.path.join(BASEDIR, 'static/upload')

# configure db
db = yaml.load(open('static/db.yaml'), Loader=yaml.FullLoader)
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def transformation(filepath, blur_path, shade_path, spread_path):
    with Image(filename=filepath) as original:
        with original.clone() as img_blur:
            img_blur.blur(radius=0, sigma=8)
            img_blur.save(filename=blur_path)
        with original.clone() as img_shade:
            img_shade.shade(gray=True, azimuth=286.0, elevation=45.0)
            img_shade.save(filename=shade_path)
        with original.clone() as img_spread:
            img_spread.spread(radius=8)
            img_spread.save(filename=spread_path)


@app.route("/api/accounts", methods=['GET', 'POST'])
def get_accounts():
    # Return all normal accounts available.
    try:
        cur = mysql.connection.cursor()
        query = 'SELECT user_name FROM users'
        cur.execute(query)
        accounts_raw = cur.fetchall()
        accounts = [account[0] for account in accounts_raw]
        cur.close()
        return jsonify({"success": True, "accounts": accounts})
    except Exception as e:
        print(e)
        return jsonify({"success": False, "error": ''})


@app.route("/api/login", methods=['POST'])
def login():
    # Login logic. Only available for normal users.
    # try:
    data = request.get_json()
    username, password = data['username'], data['password']
    cur = mysql.connection.cursor()
    query = 'SELECT user_password, user_id FROM users WHERE user_name="{}"'.format(
        username)
    cur.execute(query)
    user_data = cur.fetchone()
    hashed_password = user_data[0]
    user_id = user_data[1]
    if not hashed_password:
        raise Exception('No username matches.')
    cur.close()

    if check_password_hash(hashed_password, password):
        return jsonify({"success": True, "userid": user_id})
    # except Exception as e:
    #     print(e)
    #     return jsonify({"success": False, "error": ''})


@app.route("/api/admin_login", methods=['POST'])
def adminLogin():
    # Login logic. Only available for admin.
    try:
        data = request.get_json()
        admin_username, admin_password = data['username'], data['password']
        cur = mysql.connection.cursor()
        query = 'SELECT admin_password FROM admins WHERE admin_name="{}"'.format(
            admin_username)
        cur.execute(query)
        password = cur.fetchone()[0]
        if not password:
            raise Exception('No username matches.')
        cur.close()

        if password == admin_password:
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
        query = 'INSERT INTO users(user_name, user_password) VALUES ("{}", "{}")'.format(
            username, hashed_password)
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
    delete_username = data['username']
    cur = mysql.connection.cursor()
    query = 'DELETE FROM users WHERE user_name="{}"'.format(delete_username)
    cur.execute(query)
    mysql.connection.commit()
    cur.close()
    return jsonify({"success": True})


@app.route("/api/upload", methods=['POST'])
def upload():
    # upload files. Only available for normal users.
    f = request.files['uploadImage']
    if f and allowed_file(f.filename):
        fname = secure_filename(f.filename)
        image = '/static/upload/{}'.format(fname)
        print('filename - {}'.format(image))
        filepath = os.path.join(IMAGE_UPLOAD, fname)
        f.save(filepath)
        blur_img = '/static/upload/blur_{}'.format(fname)
        shade_img = '/static/upload/shade_{}'.format(fname)
        spread_img = '/static/upload/spread_{}'.format(fname)
        blur_path = os.path.join(IMAGE_UPLOAD, 'blur_' + fname)
        shade_path = os.path.join(IMAGE_UPLOAD, 'shade_' + fname)
        spread_path = os.path.join(IMAGE_UPLOAD, 'spread_' + fname)
        transformation(filepath, blur_path, shade_path, spread_path)
    else:
        print('Unavailable image type.')
        return jsonify({"success": False, "error": "Unavailable image type."})
    cursor = mysql.connection.cursor()
    query = "INSERT INTO image(image_path, user_id) " \
            "VALUES (%s, %s)"
    cursor.execute(query, (image, 1))
    cursor.execute(query, (blur_img, 1))
    cursor.execute(query, (shade_img, 1))
    cursor.execute(query, (spread_img, 1))
    # TODO: 拿到userid
    mysql.connection.commit()
    cursor.close()
    return jsonify({"success": True})


@app.route("/api/reset_password", methods=['POST'])
def resetPassword():
    # reset password.
    data = request.get_json()
    username, new_password = data['username'], data['password']
    new_hashed_password = generate_password_hash(new_password)
    cur = mysql.connection.cursor()
    query = 'UPDATE users SET user_password = "{}"  WHERE user_name="{}"'.format(
        new_hashed_password, username)
    cur.execute(query)
    mysql.connection.commit()
    cur.close()
    return jsonify({"success": True})


@app.route("/api/photos", methods=['POST'])
def getPhotos():
    # get all the photos of certain user.
    data = request.get_json()

    return jsonify({"result": "success"})
