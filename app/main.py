import re
from flask import render_template, request, session
from flask.helpers import url_for
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from werkzeug.utils import redirect
from app import webapp
from .MySQL_DB import mysql
import bcrypt
import MySQLdb


webapp.config['MAIL_SERVER'] = 'smtp.163.com'
webapp.config['MAIL_PORT'] = 465
webapp.config['MAIL_USE_SSL'] = True
webapp.config['MAIL_USERNAME'] = "ece1779project@163.com"
webapp.config['MAIL_PASSWORD'] = "ADHSDYQJGZCGHRWW"


# Initialize flask_mail.
mail = Mail(webapp)

# Initialize timed-url-serializer.
s = URLSafeTimedSerializer("whateversecretkey")


@webapp.route('/', methods=['GET', 'POST'])
def main():
    session.clear()
    if request.method == 'POST':
        return redirect(url_for('password_recovery'))
    elif request.method == 'GET':
        return render_template("main.html")


@webapp.route('/password_recovery', methods=['GET', 'POST'])
def password_recovery():
    if request.method == 'POST':
        username = request.form['username']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        query = "SELECT * FROM users WHERE user_name='{}'".format(username)
        cursor.execute(query)
        user = cursor.fetchone()
        user_email = user['user_email']
        cursor.close()
        token = s.dumps(user_email)
        msg = Message('Reset password for your account.',
                      sender="ece1779project@163.com", recipients=[user_email])
        link = url_for('reset_password', token=token, _external=True)
        msg.body = "Your link for reset your password is {}".format(link)
        mail.send(msg)
        return redirect(url_for('email_sent'))
    elif request.method == 'GET':
        return render_template("public/password_recovery.html")


@webapp.route('/email_sent', methods=['GET'])
def email_sent():
    return render_template("public/email_sent.html")


@webapp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    try:
        t = s.loads(token, max_age=600)
        # 异常处理之后要做一下，比如user_name没有查到等corner case.
        if request.method == 'POST':
            user_name = request.form['username']
            new_password = request.form['new_password'].encode('utf-8')
            hash_password = bcrypt.hashpw(new_password, bcrypt.gensalt())
            cursor = mysql.connection.cursor()
            query = "UPDATE users SET user_password = %s " \
                    "WHERE user_name = %s"
            cursor.execute(query, (hash_password, user_name))
            mysql.connection.commit()
            cursor.close()
            return render_template('user/user_page.html', user_name=user_name)
        elif request.method == 'GET':
            return render_template('public/reset_password.html')
    except SignatureExpired:
        return "<h1>The token is expired</h1>"


@webapp.route('/test', methods=['GET', 'POST'])
def aaa():
    return render_template("user/user_base.html")
