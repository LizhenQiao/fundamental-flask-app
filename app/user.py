from flask import render_template, request, redirect, url_for, session, flash
from app import webapp
from .MySQL_DB import mysql
import bcrypt
import MySQLdb
import os
from .utils import login_required
from werkzeug.utils import secure_filename


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'bmp'])
BASEDIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_UPLOAD = os.path.join(BASEDIR, 'static/upload')


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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

        if len(user) > 0:
            if bcrypt.hashpw(input_password, user['user_password'].encode(
                    'utf-8')) == user['user_password'].encode('utf-8'):
                session['user_name'] = input_username
                session['user_id'] = user['user_id']
                return redirect(url_for('user_page', user_name=session['user_name']))
            else:
                return "Error password or username, please contact admin"
    else:
        return render_template('user/user_login.html')


@webapp.route('/', methods=['GET', 'POST'])
def user_logout():
    session.clear()
    return render_template('main.html')


@webapp.route('/user/<string:user_name>', methods=['GET', 'POST'])
@login_required
def user_page(user_name):
    if user_name == session['user_name']:
        return render_template('user/user_page.html', user_name=session['user_name'])
    else:
        flash('url not matched')
        return redirect(url_for('main'))


@webapp.route('/user/<string:user_name>/upload', methods=['GET', 'POST'])
@login_required
def upload(user_name):
    if request.method == 'POST':
        f = request.files['img']
        if f and allowed_file(f.filename):
            fname = secure_filename(f.filename)
            image = '/static/upload/{}'.format(fname)
            print('filename - {}'.format(image))
            filepath = os.path.join(IMAGE_UPLOAD, fname)
            f.save(filepath)
        else:
            flash('Wrong image type')
            return render_template('user/user_page.html', user_name=session['user_name'])
        cursor = mysql.connection.cursor()
        query = "INSERT INTO image(image_path, user_id) " \
                "VALUES (%s, %s)"
        cursor.execute(query, (image, session['user_id']))
        mysql.connection.commit()
        cursor.close()
        return render_template('user/user_page.html', user_name=session['user_name'])
    else:
        return render_template('image/image_upload.html')


@webapp.route('/user/<string:user_name>/show', methods=['GET', 'POST'])
@login_required
def show(user_name):
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        query = "SELECT * FROM image WHERE user_id=%s"
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
        new_password = request.form['new_password'].encode('utf-8')
        hash_password = bcrypt.hashpw(new_password, bcrypt.gensalt())
        cursor = mysql.connection.cursor()
        query = "UPDATE users SET user_password = %s " \
                "WHERE user_name = %s"
        cursor.execute(query, (hash_password, session['user_name']))
        mysql.connection.commit()
        cursor.close()
        return render_template('user/user_page.html', user_name=session['user_name'])
    elif request.method == 'GET':
        return render_template('user/change_pw.html')
