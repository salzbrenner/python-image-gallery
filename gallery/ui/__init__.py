from flask import Flask
from ..data.UsersDAO import UsersDAO
from ..data.ImagesDAO import ImagesDAO
from ..data.db import get_db
import os

db = get_db()
users_dao = UsersDAO(db)
images_dao = ImagesDAO(db)


def create_app():
    app = Flask(__name__)
    app.secret_key = b'eorifjoerijffresss'
    app.config['IMAGE_BUCKET'] = os.environ.get('S3_IMAGE_BUCKET')
    app.config['REGION'] = 'us-west-1'

    from .admin.routes import admin
    from .users.routes import users

    app.register_blueprint(admin)
    app.register_blueprint(users)

    return app
