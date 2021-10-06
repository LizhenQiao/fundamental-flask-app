from flask import session, flash, redirect, url_for
from functools import wraps


def login_required(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if not any(item in session for item in ['user_name', 'admin_name']):
            print('login is required')
            return redirect(url_for('main'))
        return func(*args, **kwargs)

    return inner


def admin_required(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if not'admin_name' in session:
            print('admin user is required')
            return redirect(url_for('main'))
        return func(*args, **kwargs)

    return inner
