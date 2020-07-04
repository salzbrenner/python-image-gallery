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
from werkzeug.utils import secure_filename
from gallery.ui import images_dao
from gallery.data.S3 import upload_file
from functools import wraps


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


def app_add_image(username):
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
        file.filename = f'{username}/{secure_filename(file.filename)}'

        # image already exists
        if images_dao.get_single_image(username, file.filename):
            flash("Image already uploaded")
            return redirect(url_for('users.user_uploads',
                                    username=username))

        success = upload_file(file, current_app.config['IMAGE_BUCKET'])
        if success:
            images_dao.add_image(username, file.filename)
            flash("File uploaded")