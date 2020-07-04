from flask import Flask
from ..aws.session_secret import get_secret_flask_session
from ..data.UsersDAO import UsersDAO
from ..data.ImagesDAO import ImagesDAO
from ..data.db import get_db
import os
import json

db = get_db()
users_dao = UsersDAO(db)
images_dao = ImagesDAO(db)

# session_secret = json.loads(get_secret_flask_session())


def create_app():
    app = Flask(__name__)
    # app.secret_key = session_secret['flask_secret'].encode()
    app.secret_key = os.environ.get('FLASK_SECRET')
    app.config['IMAGE_BUCKET'] = os.environ.get('S3_IMAGE_BUCKET')
    app.config['REGION'] = 'us-west-1'

    from .admin.routes import admin
    from .users.routes import users

    app.register_blueprint(admin)
    app.register_blueprint(users)

    return app
