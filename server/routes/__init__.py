from .user_routes import create_user_routes
from .issue_routes import create_issue_routes
from .comment_routes import create_comment_routes
from flask_bcrypt import Bcrypt


def register_routes(app, bcrypt: Bcrypt):
    app.register_blueprint(create_user_routes(bcrypt=bcrypt))
    app.register_blueprint(create_issue_routes())
    app.register_blueprint(create_comment_routes())
