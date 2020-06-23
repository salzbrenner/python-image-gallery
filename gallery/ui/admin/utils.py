from flask import render_template, request, redirect, url_for, flash
from .. import db


def app_get_users():
    users = []
    for u in db.get_users():
        users.append({'username': u[0], 'full_name': u[2]})
    return users


def app_add_user():
    username = request.form['username']
    password = request.form['password']
    full_name = request.form['full_name']
    res = db.add_user(username, password, full_name)

    if res:
        flash(f'Added User {username}')
        return redirect(url_for('admin'))
    else:
        return 'No user'


def app_modify_user(user):
    password = request.form['password']
    full_name = request.form['full_name']

    res = db.edit_user(user, password, full_name)

    if res:
        flash('Updated User')
        return redirect(url_for('get_user', user=user))
    else:
        return 'No user'