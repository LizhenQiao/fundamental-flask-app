import bcrypt
from flask import render_template, request, redirect
import MySQLdb
from app import webapp
from MySQL_DB import mysql


@webapp.route('/user_login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        input_username = request.form['username']
        input_password = request.form['password'].encode('utf-8')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        query = "SELECT * FROM users WHERE user_name=%s"
        cursor.execute(query, (input_username,))
        user = cursor.fetchone()

        if len(user) > 0:
            if bcrypt.hashpw(input_password, user['user_password'].encode(
                    'utf-8')) == user['user_password'].encode('utf-8'):
                return render_template('user/user.html', user_name=user['user_name'])
            else:
                return "Error password or username, please contact admin"
    else:
        return render_template('user/user_login.html')


@webapp.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        input_adminname = request.form['adminname']
        input_password = request.form['password'].encode('utf-8')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        query = "SELECT * FROM admins WHERE admin_name=%s"
        cursor.execute(query, (input_adminname,))
        admin = cursor.fetchone()

        if len(admin) > 0:
            if bcrypt.hashpw(input_password, admin['admin_password'].encode(
                    'utf-8')) == admin['admin_password'].encode('utf-8'):
                return render_template('admin/admin.html', admin_name=admin['admin_name'])
            else:
                return "Error password or adminname"
    else:
        return render_template('admin/admin_login.html')
