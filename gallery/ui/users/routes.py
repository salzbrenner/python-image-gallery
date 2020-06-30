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
from functools import wraps
from werkzeug.utils import secure_filename
from gallery.data.S3 import upload_file, get_object

from gallery.ui import users_dao, images_dao

users = Blueprint('users', __name__)


def is_logged_in(view):
    @wraps(view)
    def decorated(**kwargs):
        if 'username' not in session or not session['username']:
            return redirect('/login')
        return view(**kwargs)
    return decorated


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}


def get_image_url(filename):
    return f'https://s3-{current_app.config["REGION"]}.amazonaws.com/{current_app.config["IMAGE_BUCKET"]}/{filename}'


@users.route('/')
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


@users.route('/u/<username>/images')
@is_logged_in
def view_images(username):
    image_paths = images_dao.get_images(username)
    images = []

    for filename in image_paths:
        obj = get_object(current_app.config['IMAGE_BUCKET'], filename)
        if obj:
            url = get_image_url(filename)
            images.append({'filename': filename, 'url': url})

    return render_template('library.html', images=images, username=username)


@users.route('/u/<username>/image/<filename>')
def view_single_image(username, filename):
    url = get_image_url(filename)
    return render_template('single_image.html', url=url)


@users.route('/u/<username>/upload', methods=['GET', 'POST'])
@is_logged_in
def user_uploads(username):
    if request.method == 'POST':

        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']

        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            file.filename = secure_filename(file.filename)

            # image already exists
            if images_dao.get_single_image(username, file.filename):
                flash("Image already uploaded")
                return redirect(url_for('users.user_uploads',
                                        username=username))

            success = upload_file(file, current_app.config['IMAGE_BUCKET'])
            if success:
                images_dao.add_image(username, file.filename)
                flash("File uploaded")

            return redirect(url_for('users.user_uploads',
                                    username=username))

    return render_template('upload.html', username=username)