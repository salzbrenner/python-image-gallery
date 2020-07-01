from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    session,
    url_for,
    flash,
    current_app
)
from gallery.data.S3 import get_object, delete_file

from gallery.ui import users_dao, images_dao
from gallery.ui.users.utils import app_add_image, is_logged_in

users = Blueprint('users', __name__)


def get_image_url(filename):
    return f'https://s3-{current_app.config["REGION"]}.amazonaws.com/{current_app.config["IMAGE_BUCKET"]}/{filename}'


@users.route('/')
@is_logged_in
def home():
    return render_template('home.html', username=session['username'])


@users.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = users_dao.get_single_user(request.form['username'])
        if user is None or user.password != request.form['password']:
            flash(f'Invalid login')
            return redirect('/login')
        else:
            session['username'] = request.form['username']
            return redirect(url_for('users.home', username=request.form['username']))
    return render_template('login.html', title='Login')


@users.route('/logout')
def logout():
    session['username'] = None
    session['is_admin'] = None
    return redirect('/login')


@users.route('/images')
@is_logged_in
def view_images():
    image_paths = images_dao.get_images(session['username'])
    images = []

    for filename in image_paths:
        obj = get_object(current_app.config['IMAGE_BUCKET'], filename)
        if obj:
            url = get_image_url(filename)
            images.append({'filename': filename, 'url': url})

    return render_template('library.html', images=images, username=session['username'])


@users.route('/delete/<filename>', methods=['POST'])
@is_logged_in
def delete_image(filename):
    res = delete_file(filename, current_app.config['IMAGE_BUCKET'])

    if res:
        images_dao.delete_image(session['username'], filename)
        flash(f'{filename} deleted')

    return redirect(url_for('users.view_images', username=session['username']))


@users.route('/upload', methods=['GET', 'POST'])
@is_logged_in
def user_uploads():
    if request.method == 'POST':
        app_add_image(session['username'])
    return render_template('upload.html', username=session['username'])