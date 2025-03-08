from flask import Flask
from config.config import Config
from models import db
from flask_bcrypt import Bcrypt
from routes import register_routes


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt = Bcrypt(app)

    register_routes(app, bcrypt)

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
