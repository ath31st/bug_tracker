from .user_routes import create_user_routes
from flask_bcrypt import Bcrypt


def register_routes(app, bcrypt: Bcrypt):
    app.register_blueprint(create_user_routes(bcrypt=bcrypt))
