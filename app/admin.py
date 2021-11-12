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

        if admin is None:
            flash('Error password or adminname', category='error')
            return render_template('admin/admin_login.html')
        else:
            if input_password == admin['admin_password']:
                session['admin_name'] = input_adminname
                return redirect(url_for('admin_page', admin_name=session['admin_name']))
            else:
                flash('Error password or adminname', category='error')
                return render_template('admin/admin_login.html')
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
        if user_details['username'] == "" or user_details['email'] == "" or user_details['password'] == "":
            flash("Error: Username, Password or Email can't be empty!", category='error')
            return render_template('admin/register.html')
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
        flash('Register Successfully', category='info')
        return render_template('admin/register.html')
    else:
        return render_template('admin/register.html')


@webapp.route('/admin/list', methods=['GET'])
# Display an HTML list of all users.
def user_list():
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM users"
    cursor.execute(query)
    return render_template("admin/list.html", cursor=cursor)


@webapp.route('/admin/delete/<int:user_id>', methods=['GET', 'POST'])
@admin_required
def delete(user_id):
    cursor = mysql.connection.cursor()
    query = "DELETE FROM users WHERE user_id = %s"
    cursor.execute(query, (user_id,))
    mysql.connection.commit()
    return redirect(url_for('user_list'))


@webapp.route('/admin/edit/<int:user_id>', methods=['GET'])
@admin_required
def edit(user_id):
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM users WHERE user_id = %s"
    cursor.execute(query, (user_id,))
    row = cursor.fetchone()
    user_id = row[0]
    name = row[1]
    email = row[3]

    return render_template("admin/edit.html", user_id=user_id, name=name, email=email)


@webapp.route('/admin/edit/<int:user_id>', methods=['POST'])
def edit_save(user_id):
    name = request.form.get('name', "")
    email = request.form.get('email', "")

    if name == "" or email == "":
        flash("Error: All fields are required!", category='error')
        return render_template("admin/edit.html", user_id=user_id, name=name, email=email)
    else:
        cursor = mysql.connection.cursor()
        query = "UPDATE users SET user_name=%s, user_email=%s " \
                "WHERE user_id = %s"

        cursor.execute(query, (name, email, user_id))
        mysql.connection.commit()

        return redirect(url_for('user_list'))


@webapp.route('/admin/logout', methods=['GET', 'POST'])
def admin_logout():
    session.clear()
    return redirect(url_for("main"))
