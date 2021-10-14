from flask import render_template, request, redirect, flash, url_for, session
from app import webapp
from .MySQL_DB import mysql
import bcrypt
import MySQLdb
from .utils import admin_required


@webapp.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        session.pop('admin_name', None)
        input_adminname = request.form['adminname']
        input_password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        query = "SELECT * FROM admins WHERE admin_name=%s"
        cursor.execute(query, (input_adminname,))
        admin = cursor.fetchone()
        if len(admin) > 0:
            if input_password == admin['admin_password']:
                session['admin_name'] = input_adminname
                return redirect(url_for('admin_page', admin_name=session['admin_name']))
            else:
                return "Error password or adminname"
    else:
        return render_template('admin/admin_login.html')


@webapp.route('/admin/<string:admin_name>', methods=['GET', 'POST'])
@admin_required
def admin_page(admin_name):
    return render_template('admin/admin_page.html', admin_name=admin_name)


@webapp.route('/admin/register', methods=['GET', 'POST'])
@admin_required
def register():
    if request.method == 'POST':
        user_details = request.form
        username = user_details['username']
        email = user_details['email']
        password = user_details['password'].encode('utf-8')
        hash_password = bcrypt.hashpw(password, bcrypt.gensalt())
        cursor = mysql.connection.cursor()
        query = "INSERT INTO users(user_name, user_password, user_email) " \
                "VALUES (%s, %s, %s)"
        cursor.execute(query, (username, hash_password, email))
        mysql.connection.commit()
        cursor.close()
        session['user_name'] = username
        flash('successfully register')
        return render_template('admin/admin_page.html', username=username)
    else:
        return render_template('admin/register.html')


@webapp.route('/admin/<string:admin_name>/delete', methods=['GET', 'POST'])
@admin_required
# TODO: 有空的话delete和update也可以改成交互式，而不是手工输入userid
def delete(admin_name):
    cursor = mysql.connection.cursor()
    query1 = "SELECT `user_id`, `user_name` FROM users"
    cursor.execute(query1)
    session['users'] = cursor.fetchall()
    if request.method == 'POST':
        delete_id = request.form['delete_id']
        query2 = "DElETE FROM users WHERE user_id = %s"
        cursor.execute(query2, delete_id)
        mysql.connection.commit()
        cursor.close()
        flash('successfully delete')
        return render_template('admin/admin_page.html', admin_name=admin_name)
    elif request.method == 'GET':
        return render_template('admin/delete.html', users=session['users'], admin_name=admin_name)


@webapp.route('/admin/<string:admin_name>/update', methods=['GET', 'POST'])
@admin_required
# TODO: 有空的话delete和update也可以改成交互式，而不是手工输入userid
def update(admin_name):
    if request.method == 'POST':
        update_id = request.form['update_id']
        update_name = request.form['update_name']
        update_password = request.form['update_password'].encode('utf-8')
        hash_password = bcrypt.hashpw(update_password, bcrypt.gensalt())
        cursor = mysql.connection.cursor()
        query1 = "UPDATE users SET user_name = %s, user_password = %s " \
                 "WHERE user_id = %s"
        cursor.execute(query1, (update_name, hash_password, update_id))
        mysql.connection.commit()
        query2 = "SELECT `user_id`, `user_name` FROM users"
        cursor.execute(query2)
        session['users'] = cursor.fetchall()
        cursor.close()
        flash('successfully update')
        return render_template('admin/admin_page.html', admin_name=admin_name)
    elif request.method == 'GET':
        return render_template('admin/update.html', users=session['users'], admin_name=admin_name)


@webapp.route('/user/logout', methods=['GET', 'POST'])
def admin_logout():
    session.clear()
    return redirect(url_for("main"))
