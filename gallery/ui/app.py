from flask import Flask, render_template, request, redirect, url_for, flash
# from tools.db import get_users, connect, get_single_user, edit_user, delete_user, add_user
from .controller import app_get_users, app_modify_user, app_add_user, get_single_user, delete_user
from tools.db import connect

# connect to DB
connect()

app = Flask(__name__)
app.secret_key=b'asodifj983274**Dosj'


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/admin')
def admin():
    return render_template('admin.html', users=app_get_users())


@app.route('/admin/user/<user>', methods=['GET', 'POST'])
def get_user(user):
    if request.method == 'POST':
        return app_modify_user(user)

    u = get_single_user(user)
    return render_template('user.html', user=u)


@app.route('/admin/add-user', methods=['GET', 'POST'])
def add_user_route():
    if request.method == 'POST':
        return app_add_user()

    return render_template('add_user.html')


@app.route('/admin/delete-confirm/<user>')
def delete_confirm(user):
    u = get_single_user(user)
    return render_template('delete_confirm.html', user=u)


@app.route('/admin/delete/<user>', methods=['POST'])
def delete_handler(user):
    res = delete_user(user)
    if res:
        flash(f'{user} deleted')
        return redirect(url_for('admin'))
    else:
        return redirect(url_for('get_user', user=user))

#
# @app.route('/')
# def hello_world():
#     return 'Hello, World!'
#
# #
# # @app.route('/admin')
# # def admin():
# #     users = []
# #     for u in get_users():
# #         users.append({'username': u[0], 'full_name': u[2]})
# #     return render_template('admin.html', users=users)
# #
# #
# # @app.route('/admin/user/<user>', methods=['GET', 'POST'])
# # def get_user(user):
# #     if request.method == 'POST':
# #         return modify_user(user)
# #
# #     u = get_single_user(user)
# #
# #     return render_template('user.html',
# #                            user=u)
# #

# @app.route('/admin/add-user', methods=['GET', 'POST'])
# def add_user_route():
#     if request.method == 'POST':
#         return app_add_user()
#
#     return render_template('add_user.html')

#
# def app_add_user():
#     username = request.form['username']
#     password = request.form['password']
#     full_name = request.form['full_name']
#     res = add_user(username, password, full_name)
#
#     if res:
#         flash(f'Added User {username}')
#         return redirect(url_for('admin'))
#     else:
#         return 'No user'
#
#
# def modify_user(user):
#     username = request.form['username']
#     password = request.form['password']
#     full_name = request.form['full_name']
#
#     res = edit_user(username, password, full_name)
#
#     if res:
#         flash('Updated User')
#         return redirect(url_for('get_user', user=user))
#     else:
#         return 'No user'
#

# @app.route('/admin/delete-confirm/<user>')
# def delete_confirm(user):
#     u = get_single_user(user)
#     return render_template('delete_confirm.html', user=u)


# @app.route('/admin/delete/<user>', methods=['POST'])
# def delete_handler(user):
#     res = delete_user(user)
#     if res:
#         flash(f'{user} deleted')
#         return redirect(url_for('admin'))
#     else:
#         return redirect(url_for('get_user', user=user))


# @app.route('/admin/<user>')
if __name__ == '__main__':
    app.run(debug=True)