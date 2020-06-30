from flask import Flask
import json
from ..aws.session_secret import get_secret_flask_session
from ..data.UsersDAO import UsersDAO
from ..data.db import connect

session_secret = json.loads(get_secret_flask_session())
db = connect()
users_dao = UsersDAO(db)


def create_app():
    app = Flask(__name__)
    app.secret_key = session_secret['flask_secret'].encode()

    from .admin.routes import admin
    from .users.routes import users

    app.register_blueprint(admin)
    app.register_blueprint(users)

    return app
