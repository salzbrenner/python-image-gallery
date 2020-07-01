from flask import (
    render_template,
    url_for,
    flash,
    redirect,
    request,
    abort,
    Blueprint,
    session
)
from .. import users_dao
from .utils import app_modify_user, app_add_user, authenticate_admin


admin = Blueprint('admin', __name__)


@admin.route('/admin')
def admin_redirect():
    return redirect('/admin/users')


@admin.route('/admin/users')
@authenticate_admin
def admin_home():
    return render_template('admin.html', users=users_dao.get_users())


@admin.route('/admin/user/<user>', methods=['GET', 'POST'])
@authenticate_admin
def get_user(user):
    if request.method == 'POST':
        return app_modify_user(user)
    u = users_dao.get_single_user(user)
    return render_template('user.html', user=u)


@admin.route('/admin/add-user', methods=['GET', 'POST'])
@authenticate_admin
def add_user_route():
    if request.method == 'POST':
        return app_add_user()
    return render_template('add_user.html')


@admin.route('/admin/delete-confirm/<user>')
@authenticate_admin
def delete_confirm(user):
    u = users_dao.get_single_user(user)
    return render_template('delete_confirm.html', user=u)


@admin.route('/admin/delete/<user>', methods=['POST'])
@authenticate_admin
def delete_handler(user):
    res = users_dao.delete_user(user)
    if res:
        flash(f'{user} deleted')
        return redirect(url_for('admin.admin_home'))
    else:
        return redirect(url_for('admin.get_user', user=user))

