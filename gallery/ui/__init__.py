from flask import Flask
import json
from ..aws.session_secret import get_secret_flask_session
from ..data.UsersDAO import UsersDAO
from ..data.ImagesDAO import ImagesDAO
from ..data.db import connect

session_secret = json.loads(get_secret_flask_session())
db = connect()
users_dao = UsersDAO(db)
images_dao = ImagesDAO(db)


def create_app():
    app = Flask(__name__)
    app.secret_key = session_secret['flask_secret'].encode()
    app.config['IMAGE_BUCKET'] = 'evan.au.cc.image-gallery'
    app.config['REGION'] = 'us-west-1'

    from .admin.routes import admin
    from .users.routes import users

    app.register_blueprint(admin)
    app.register_blueprint(users)

    return app
