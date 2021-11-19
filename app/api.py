import urllib
from flask import request, jsonify
from app import webapp
from .MySQL_DB import mysql
import bcrypt
import MySQLdb
import os
from werkzeug.utils import secure_filename
from wand.image import Image
import random
import boto3
from .config import S3_KEY, S3_SECRET, S3_BUCKET, S3_LOCATION
s3 = boto3.client(
    "s3",
    aws_access_key_id=S3_KEY,
    aws_secret_access_key=S3_SECRET
)

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'bmp'])
BASEDIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_UPLOAD = os.path.join(BASEDIR, 'static/upload')


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_available_filename(filename):
    clean_filename = filename.rsplit('.', 1)[0].lower()
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    query = "SELECT * FROM images"
    cursor.execute(query)
    images = cursor.fetchall()
    if not images:
        return filename
    for image in images:
        clean_imagename = image["image_path"].rsplit(
            '/', 1)[1].rsplit('.', 1)[0]
        if clean_imagename == clean_filename:
            return clean_filename + str(random.randint(10 ** 9 + 1, 10 ** 10)) + '.' + filename.rsplit('.', 1)[1].lower()
    return filename


def transformation(url, blur_name, shade_name, spread_name, blur_path, shade_path, spread_path, filetype):
    response = urllib.request.urlopen(url)
    with Image(file=response) as original:
        with original.clone() as img_blur:
            img_blur.blur(radius=0, sigma=8)
            img_blur.save(filename=blur_path)
        with original.clone() as img_shade:
            img_shade.shade(gray=True, azimuth=286.0, elevation=45.0)
            img_shade.save(filename=shade_path)
        with original.clone() as img_spread:
            img_spread.spread(radius=8)
            img_spread.save(filename=spread_path)
    with open(blur_path, "rb") as f:
        s3.upload_fileobj(f, S3_BUCKET, blur_name, ExtraArgs={'ACL': 'public-read', 'ContentType': filetype})
    with open(shade_path, "rb") as f:
        s3.upload_fileobj(f, S3_BUCKET, shade_name, ExtraArgs={'ACL': 'public-read', 'ContentType': filetype})
    with open(spread_path, "rb") as f:
        s3.upload_fileobj(f, S3_BUCKET, spread_name, ExtraArgs={'ACL': 'public-read', 'ContentType': filetype})


@webapp.route("/api/register", methods=['POST'])
def register_api():
    # Add new user accounts. Only available for admin.
    try:
        data = request.get_json()
        if data['username'] == "" or data['password'] == "":
            return jsonify({
                "success": False,
                "error": {
                    "code": 10000,
                    "message": "Invalid input: Username, Password or Email can't be empty!"
                }
            })
        username = data['username']
        email = data['email'] if 'email' in data else ''
        password = data['password'].encode('utf-8')
        hash_password = bcrypt.hashpw(password, bcrypt.gensalt())
        cur = mysql.connection.cursor()
        query = 'INSERT INTO users(user_name, user_password, user_email) VALUES ("{}", "{}", "{}")'.format(
            username, hash_password, email)
        cur.execute(query)
        mysql.connection.commit()
        cur.close()
        return jsonify({"success": True})
    except Exception as e:
        print(e)
        return jsonify({
            "success": False,
            "error": {
                "code": 500,
                "message": "Internal Server Error!"
            }
        })


@webapp.route("/api/upload", methods=['POST'])
def upload_api():
    # upload files. Only available for normal users.
    try:
        f = request.files['file']
        name = request.form['name']
        input_password = request.form['password'].encode('utf-8')
        f.seek(0, 2)
        file_length = f.tell()
        if file_length > 1024*1024:
            return jsonify({"success": False, "error": {
                "code": 10003,
                "message": "Image too large. Upload limit is 1Mb."
            }})
        # set the cursor back to the original position
        f.seek(0)
        if f and allowed_file(f.filename):
            available_fname = get_available_filename(f.filename)
            fname = secure_filename(available_fname)
            filepath = os.path.join(IMAGE_UPLOAD, fname)
            f.save(filepath)
            file_size = os.stat(filepath).st_size
            ftype = fname.rsplit('.', 1)[1].lower()
            s3.upload_fileobj(f, S3_BUCKET, fname, ExtraArgs={'ACL': 'public-read', 'ContentType': ftype})
            url_o = S3_LOCATION + fname
            blur_name = 'blur_{}'.format(fname)
            shade_name = 'shade_{}'.format(fname)
            spread_name = 'spread_{}'.format(fname)
            blur_path = os.path.join(IMAGE_UPLOAD, blur_name)
            shade_path = os.path.join(IMAGE_UPLOAD, shade_name)
            spread_path = os.path.join(IMAGE_UPLOAD, spread_name)
            transformation(url_o, blur_name, shade_name, spread_name, blur_path, shade_path, spread_path, ftype)
            blur_size = os.stat(blur_path).st_size
            shade_size = os.stat(shade_path).st_size
            spread_size = os.stat(spread_path).st_size
            os.remove(filepath)
            os.remove(blur_path)
            os.remove(shade_path)
            os.remove(spread_path)
            url_blur = S3_LOCATION + blur_name
            url_shade = S3_LOCATION + shade_name
            url_spread = S3_LOCATION + spread_name
        else:
            print('Unavailable image type.')
            return jsonify({"success": False, "error": {
                "code": 10000,
                "message": "Unavailable image format."
            }})
        cursor0 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        query = "SELECT * FROM users WHERE user_name=%s"
        cursor0.execute(query, (name,))
        user = cursor0.fetchone()
        try:
            if bcrypt.hashpw(input_password, user['user_password'].encode(
                    'utf-8')) == user['user_password'].encode('utf-8'):
                user_id = user["user_id"]
            else:
                return jsonify({
                    "success": False,
                    "error": {
                        "code": 10002,
                        "message": "Password or username wrong."
                    }
                })
        except:
            return jsonify({
                "success": False,
                "error": {
                    "code": 10002,
                    "message": "Password or username wrong."
                }
            })
        cursor = mysql.connection.cursor()
        query = "INSERT INTO images(image_path, user_id) " \
                "VALUES (%s, %s)"
        cursor.execute(query, (url_o, user_id))
        cursor.execute(query, (url_blur, user_id))
        cursor.execute(query, (url_shade, user_id))
        cursor.execute(query, (url_spread, user_id))
        mysql.connection.commit()
        cursor.close()
        return jsonify({
            "success": True,
            "payload": {
                "original_size": file_size,
                "blur_size": blur_size,
                "shade_size": shade_size,
                "spread_size": spread_size
            }
        })
    except:
        return jsonify({
            "success": False,
            "error": {
                "code": 500,
                "message": "Internal Server Error!"
            }
        })
