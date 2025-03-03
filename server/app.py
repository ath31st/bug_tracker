from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config.config import Config

app = Flask(__name__)

app.config.from_object(Config)

db = SQLAlchemy(app)


def main():
    app.run(debug=True)


if __name__ == "__main__":
    main()
