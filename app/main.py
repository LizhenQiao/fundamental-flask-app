from flask import render_template, request, session
from flask.helpers import url_for
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from werkzeug.utils import redirect
from app import webapp
from .MySQL_DB import mysql
import bcrypt


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
        return redirect(url_for('email_sent'))
    elif request.method == 'GET':
        return render_template("main.html")


@webapp.route('/email_sent', methods=['GET'])
# TODO: recipients 从数据库里取，而不是目前写死的948090427@qq.com
def email_sent():
    token = s.dumps("948090427@qq.com")
    msg = Message('Reset password for your account.',
                  sender="ece1779project@163.com", recipients=["948090427@qq.com"])
    link = url_for('reset_password', token=token, _external=True)
    msg.body = "Your link for reset your password is {}".format(link)
    mail.send(msg)
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
            return render_template('user/change_pw.html')
    except SignatureExpired:
        return "<h1>The token is expired</h1>"


@webapp.route('/reset_password', methods=['GET', 'POST'])
def aa():
    try:
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
            return render_template('user/reset_password.html')
    except SignatureExpired:
        return "<h1>The token is expired</h1>"
