from flask import request, jsonify
from app import webapp
from .MySQL_DB import mysql
import bcrypt
import MySQLdb
import os
from werkzeug.utils import secure_filename
from wand.image import Image
import random

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


@webapp.route("/api/register", methods=['POST'])
def register_api():
    # Add new user accounts. Only available for admin.
    try:
        data = request.get_json()
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
        # TODO: 在接口获取错误码
        print(e)
        return jsonify({"success": False, "error": ''})


@webapp.route("/api/upload", methods=['POST'])
def upload_api():
  # TODO: 暂时没有测试
    # upload files. Only available for normal users.
    f = request.files['uploadImage']
    if f and allowed_file(f.filename):
        available_fname = get_available_filename(f.filename)
        fname = secure_filename(available_fname)
        image = '/static/upload/{}'.format(fname)
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
    mysql.connection.commit()
    cursor.close()
    # TODO: 怎么获取到这些图片的size, original_size印象中form-data里有可能取得到
    return jsonify({
        "success": True,
        "payload": {
            "original_size": 1,
            "blur_size": 1,
            "shade_size": 1,
            "spread_size": 1
        }
    })
