from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    session,
    url_for,
    flash
)

from gallery.ui import users_dao

users = Blueprint('users', __name__)


@users.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print(request.form)
        user = users_dao.get_single_user(request.form['username'])
        if user is None or user.password != request.form['password']:
            flash(f'Invalid login')
            return redirect('/login')
        else:
            session['username'] = request.form['username']
            return redirect(url_for('admin.get_user', user=request.form['username']))
    # if current_user.is_authenticated:
    #     return redirect(url_for('main.home'))
    #
    # form = LoginForm()
    # if form.validate_on_submit():
    #     user = User.query.filter_by(email=form.email.data).first()
    #     if user and bcrypt.check_password_hash(user.password, form.password.data):
    #         login_user(user, remember=form.remember.data)
    #         next_page = request.args.get('next')
    #         return redirect(next_page) if next_page else redirect(url_for('main.home'))
    #     else:
    #         flash('Login unsuccessful', 'danger')
    return render_template('login.html', title='Login')


@users.route('/logout')
def logout():
    session['username'] = None
    session['is_admin'] = None
    return redirect('/login')

