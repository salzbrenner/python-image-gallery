from flask import (
    render_template,
    url_for,
    flash,
    redirect,
    request,
    abort,
    Blueprint
)
from .. import db
from .utils import app_modify_user, app_get_users, app_add_user


admin = Blueprint('posts', __name__)


@admin.route('/')
def hello_world():
    return 'Hello, World!'


@admin.route('/admin')
def admin():
    return render_template('admin.html', users=app_get_users())


@admin.route('/admin/user/<user>', methods=['GET', 'POST'])
def get_user(user):
    if request.method == 'POST':
        return app_modify_user(user)
    u = db.get_single_user(user)
    return render_template('user.html', user=u)


@admin.route('/admin/add-user', methods=['GET', 'POST'])
def add_user_route():
    if request.method == 'POST':
        return app_add_user()
    return render_template('add_user.html')


@admin.route('/admin/delete-confirm/<user>')
def delete_confirm(user):
    u = db.get_single_user(user)
    return render_template('delete_confirm.html', user=u)


@admin.route('/admin/delete/<user>', methods=['POST'])
def delete_handler(user):
    res = db.delete_user(user)
    if res:
        flash(f'{user} deleted')
        return redirect(url_for('admin'))
    else:
        return redirect(url_for('get_user', user=user))