from flask import render_template, request, redirect, flash, url_for
from app import webapp
from MySQL_DB import mysql
import bcrypt


@webapp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_details = request.form
        username = user_details['username']
        password = user_details['password'].encode('utf-8')
        hash_password = bcrypt.hashpw(password, bcrypt.gensalt())

        cursor = mysql.connection.cursor()
        query = "INSERT INTO users(user_name, user_password) " \
                "VALUES (%s, %s)"
        cursor.execute(query, (username, hash_password))
        mysql.connection.commit()
        cursor.close()
        flash('successfully register')
        return redirect(url_for('admin'))
    else:
        return render_template('admin/register.html')


@webapp.route('/delete', methods=['GET', 'POST'])
def delete():
    cursor = mysql.connection.cursor()
    query1 = "SELECT `user_id`, `user_name` FROM users"
    cursor.execute(query1)
    users = cursor.fetchall()
    if request.method == 'POST':
        delete_id = request.form['user_id']
        query2 = "DElETE * FROM %s WHERE user_id = %s"
        cursor.execute(query2 % (users, delete_id))
        mysql.connection.commit()
        cursor.close()
        flash('successfully delete')
        return redirect(url_for('admin'))
    else:
        return render_template('admin/delete.html', users=users)


@webapp.route('/update', methods=['GET', 'POST'])



