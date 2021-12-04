from flask import Flask
import flask_sqlalchemy

from . import config


def create_app():
    flask_app = Flask(__name__)
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_CONNECTION_URI
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    flask_app.config['SECRET_KEY'] = config.secret
    flask_app.app_context().push()
    #db1 = flask_sqlalchemy.SQLAlchemy(flask_app)
    #db1.init_app(flask_app)
    return flask_app


app = create_app()