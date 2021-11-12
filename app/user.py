from flask import render_template, request, redirect, url_for, session, flash
from app import webapp
from .MySQL_DB import mysql
import boto3
import bcrypt
import MySQLdb
import os
import urllib.request
import validators
from urllib.parse import urlparse
from .utils import login_required
from werkzeug.utils import secure_filename
from wand.image import Image
from io import StringIO
import random
from config import S3_KEY, S3_SECRET, S3_BUCKET, S3_LOCATION
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
    user_id = session['user_id']
    clean_filename = filename.rsplit('.', 1)[0].lower()
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    query = "SELECT * FROM images WHERE user_id='{}'".format(user_id)
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


@webapp.route('/user', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        session.pop('user_name', None)
        input_username = request.form['username']
        input_password = request.form['password'].encode('utf-8')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        query = "SELECT * FROM users WHERE user_name=%s"
        cursor.execute(query, (input_username,))
        user = cursor.fetchone()

        if user is None:
            flash('Error password or username, please try again', category='error')
            return render_template('user/user_login.html')
        else:
            if bcrypt.hashpw(input_password, user['user_password'].encode(
                    'utf-8')) == user['user_password'].encode('utf-8'):
                session['user_name'] = input_username
                session['user_id'] = user['user_id']
                return redirect(url_for('user_page', user_name=session['user_name']))
            else:
                flash('Error password or username, please try again', category='error')
                return render_template('user/user_login.html')
    else:
        return render_template('user/user_login.html')


@webapp.route('/user/<string:user_name>', methods=['GET', 'POST'])
@login_required
def user_page(user_name):
    if user_name == session['user_name']:
        return render_template('user/user_page.html', user_name=session['user_name'])
    else:
        flash('url not matched', category='error')
        return redirect(url_for('main'))


@webapp.route('/user/<string:user_name>/upload', methods=['GET', 'POST'])
@login_required
# def upload(user_name):
#     if request.method == 'POST':
#         if request.files['img']:
#             f = request.files['img']
#             # set the cursor to the file's position
#             f.seek(0, 2)
#             file_length = f.tell()
#             if file_length > 1024*1024:
#                 flash('Error:Image size is too large', category='error')
#                 return render_template('image/image_upload.html')
#             # set the cursor back to the original position
#             f.seek(0)
#             if f and allowed_file(f.filename):
#                 available_fname = get_available_filename(f.filename)
#                 fname = secure_filename(available_fname)
#                 image = '/static/upload/{}'.format(fname)
#                 filepath = os.path.join(IMAGE_UPLOAD, fname)
#                 s3.upload_fileobj(f, S3_BUCKET, fname,
#                                   ExtraArgs={'ACL': 'public-read'})
#                 url_origin = S3_LOCATION + fname
#                 blur_img = '/static/upload/blur_{}'.format(fname)
#                 shade_img = '/static/upload/shade_{}'.format(fname)
#                 spread_img = '/static/upload/spread_{}'.format(fname)
#                 blur_path = os.path.join(IMAGE_UPLOAD, 'blur_' + fname)
#                 shade_path = os.path.join(IMAGE_UPLOAD, 'shade_' + fname)
#                 spread_path = os.path.join(IMAGE_UPLOAD, 'spread_' + fname)
#                 transformation(url_origin, blur_path, shade_path, spread_path)
#             else:
#                 flash('Error:Wrong image type', category='error')
#                 return render_template('image/image_upload.html')
# #             cursor = mysql.connection.cursor()
# #             query = "INSERT INTO images(image_path, user_id) " \
# #                     "VALUES (%s, %s)"
# #             cursor.execute(query, (image, session['user_id']))
# #             cursor.execute(query, (blur_img, session['user_id']))
# #             cursor.execute(query, (shade_img, session['user_id']))
# #             cursor.execute(query, (spread_img, session['user_id']))
# #             mysql.connection.commit()
# #             cursor.close()
# #             flash('Upload by local files Successfully', category='info')
# #             return render_template('image/image_upload.html')
# #         else:
# #             url = request.form['image_url']
# #             if validators.url(url):
# #                 file_length = urllib.request.urlopen(url).length
# #                 if file_length > 1024*1024:
# #                     flash('Error:Image size is too large', category='error')
# #                     return render_template('image/image_upload.html')
# #                 file = urlparse(url)
# #                 filename = os.path.basename(file.path)
# #                 url_image = "/static/upload/" + filename
# #                 filepath = os.path.join(IMAGE_UPLOAD, filename)
# #                 urllib.request.urlretrieve(url, filepath)
# #                 blur_img = '/static/upload/blur_{}'.format(filename)
# #                 shade_img = '/static/upload/shade_{}'.format(filename)
# #                 spread_img = '/static/upload/spread_{}'.format(filename)
# #                 blur_path = os.path.join(IMAGE_UPLOAD, 'blur_' + filename)
# #                 shade_path = os.path.join(IMAGE_UPLOAD, 'shade_' + filename)
# #                 spread_path = os.path.join(IMAGE_UPLOAD, 'spread_' + filename)
# #                 transformation(filepath, blur_path, shade_path, spread_path)
# #                 s3.upload_fileobj(filepath, S3_BUCKET, fname,
# #                                   ExtraArgs={'ACL': 'public-read'})
# #                 cursor = mysql.connection.cursor()
# #                 query = "INSERT INTO images(image_path, user_id) " \
# #                     "VALUES (%s, %s)"
# #                 cursor.execute(query, (url_image, session['user_id']))
# #                 cursor.execute(query, (blur_img, session['user_id']))
# #                 cursor.execute(query, (shade_img, session['user_id']))
# #                 cursor.execute(query, (spread_img, session['user_id']))
# #                 mysql.connection.commit()
# #                 cursor.close()
# #                 flash('Upload by URL successfully', category='info')
# #                 return render_template('image/image_upload.html')
# #             else:
# #                 flash('Error:Wrong URL', category='error')
# #                 return render_template('image/image_upload.html')
#     else:
#         return render_template('image/image_upload.html')
#
#
# def transformation(url_origin, blur_path, shade_path, spread_path):
#     response = urllib.request.urlopen(url_origin)
#     with Image(filename=response) as original:
#         with original.clone() as img_blur:
#             img_blur.blur(radius=0, sigma=8)
#             img_blur.save(filename=blur_path)
#         with original.clone() as img_shade:
#             img_shade.shade(gray=True, azimuth=286.0, elevation=45.0)
#             img_shade.save(filename=shade_path)
#         with original.clone() as img_spread:
#             img_spread.spread(radius=8)
#             img_spread.save(filename=spread_path)

def upload(user_name):
    if request.method == 'POST':
        if request.files['img']:
            f = request.files['img']
            # set the cursor to the file's position
            f.seek(0, 2)
            file_length = f.tell()
            if file_length > 1024*1024:
                flash('Error:Image size is too large', category='error')
                return render_template('image/image_upload.html')
            # set the cursor back to the original position
            f.seek(0)
            if f and allowed_file(f.filename):
                available_fname = get_available_filename(f.filename)
                fname = secure_filename(available_fname)
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
                url_blur = S3_LOCATION + blur_name
                url_shade = S3_LOCATION + shade_name
                url_spread = S3_LOCATION + spread_name
            else:
                flash('Error:Wrong image type', category='error')
                return render_template('image/image_upload.html')
            cursor = mysql.connection.cursor()
            query = "INSERT INTO images(image_path, user_id) " \
                    "VALUES (%s, %s)"
            cursor.execute(query, (url_o, session['user_id']))
            cursor.execute(query, (url_blur, session['user_id']))
            cursor.execute(query, (url_shade, session['user_id']))
            cursor.execute(query, (url_spread, session['user_id']))
            mysql.connection.commit()
            cursor.close()
            flash('Upload by local files Successfully', category='info')
            return render_template('image/image_upload.html')
        else:
            url = request.form['image_url']
            if validators.url(url):
                file_length = urllib.request.urlopen(url).length
                if file_length > 1024*1024:
                     flash('Error:Image size is too large', category='error')
                     return render_template('image/image_upload.html')
                file = urlparse(url)
                filename = os.path.basename(file.path)
                filetype = filename.rsplit('.', 1)[1].lower()
                # url_image = "/static/upload/" + filename
                filepath = os.path.join(IMAGE_UPLOAD, filename)
                urllib.request.urlretrieve(url, filepath)
                with open(filepath, "rb") as f:
                    s3.upload_fileobj(f, S3_BUCKET, filename, ExtraArgs={'ACL': 'public-read', 'ContentType': filetype})
                url_o = S3_LOCATION + filename
                os.remove(filepath)
                blur_path = os.path.join(IMAGE_UPLOAD, 'blur_' + filename)
                shade_path = os.path.join(IMAGE_UPLOAD, 'shade_' + filename)
                spread_path = os.path.join(IMAGE_UPLOAD, 'spread_' + filename)
                blur_name = 'blur_{}'.format(filename)
                shade_name = 'shade_{}'.format(filename)
                spread_name = 'spread_{}'.format(filename)
                url_blur = S3_LOCATION + blur_name
                url_shade = S3_LOCATION + shade_name
                url_spread = S3_LOCATION + spread_name
                transformation(url_o, blur_name, shade_name, spread_name, blur_path, shade_path, spread_path, filetype)
                cursor = mysql.connection.cursor()
                query = "INSERT INTO images(image_path, user_id) " \
                        "VALUES (%s, %s)"
                cursor.execute(query, (url_o, session['user_id']))
                cursor.execute(query, (url_blur, session['user_id']))
                cursor.execute(query, (url_shade, session['user_id']))
                cursor.execute(query, (url_spread, session['user_id']))
                mysql.connection.commit()
                cursor.close()
                flash('Upload by URL successfully', category='info')
                return render_template('image/image_upload.html')
            else:
                flash('Error:Wrong URL', category='error')
                return render_template('image/image_upload.html')
    else:
        return render_template('image/image_upload.html')


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
    os.remove(blur_path)
    with open(shade_path, "rb") as f:
        s3.upload_fileobj(f, S3_BUCKET, shade_name, ExtraArgs={'ACL': 'public-read', 'ContentType': filetype})
    os.remove(shade_path)
    with open(spread_path, "rb") as f:
        s3.upload_fileobj(f, S3_BUCKET, spread_name, ExtraArgs={'ACL': 'public-read', 'ContentType': filetype})
    os.remove(spread_path)


@webapp.route('/user/<string:user_name>/show', methods=['GET', 'POST'])
@login_required
# 图片展示UI考虑加一个×号返回上一级
def show(user_name):
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        query = "SELECT * FROM images WHERE user_id=%s"
        cursor.execute(query, (session['user_id'],))
        images = cursor.fetchall()
    except Exception as e:
        print(e)
        return 'Exception : Cannot get the upload images list'
    return render_template("image/image_show.html", images=images)


@webapp.route('/user/<string:user_name>/change_pw', methods=['GET', 'POST'])
@login_required
def change_pw(user_name):
    if request.method == 'POST':
        if request.form['new_password'] == '':
            flash("Error:Password can't be empty", category='error')
            return render_template('user/change_pw.html')
        else:
            new_password = request.form['new_password'].encode('utf-8')
            hash_password = bcrypt.hashpw(new_password, bcrypt.gensalt())
            cursor = mysql.connection.cursor()
            query = "UPDATE users SET user_password = %s " \
                    "WHERE user_name = %s"
            cursor.execute(query, (hash_password, session['user_name']))
            mysql.connection.commit()
            cursor.close()
            flash('Password change Successfully', category='info')
            return render_template('user/change_pw.html', user_name=session['user_name'])
    elif request.method == 'GET':
        return render_template('user/change_pw.html')


@webapp.route('/user/logout', methods=['GET', 'POST'])
def user_logout():
    session.clear()
    return redirect(url_for("main"))
