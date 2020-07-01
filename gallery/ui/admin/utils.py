from flask import render_template, request, redirect, url_for, flash, session
from functools import wraps
from .. import users_dao


def check_admin():
    return 'username' in session and (session['username'] == 'evan' or session['username'] == 'dongji')


def authenticate_admin(view):
    @wraps(view)
    def decorated(**kwargs):
        if not check_admin():
            return redirect('/login')
        session['is_admin'] = True
        return view(**kwargs)
    return decorated


def app_add_user():
    username = request.form['username']
    password = request.form['password']
    full_name = request.form['full_name']
    res = users_dao.add_user(username, password, full_name)

    if res:
        flash(f'Added User {username}')
        return redirect(url_for('admin.admin_home'))
    else:
        return 'No user'


def app_modify_user(user):
    password = request.form['password']
    full_name = request.form['full_name']

    res = users_dao.edit_user(user, password, full_name)

    if res:
        flash('Updated User')
        return redirect(url_for('admin.get_user', user=user))
    else:
        return 'No user'