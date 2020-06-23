from flask import Flask
from ..data.UsersDAO import UsersDAO

db = UsersDAO()


def create_app():
    app = Flask(__name__)
    app.secret_key = b'asodifj983274**Dosj'

    from .admin.routes import admin

    app.register_blueprint(admin)

    return app
