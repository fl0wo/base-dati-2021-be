from flask import Flask
import flask_sqlalchemy
import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

from . import config

UPLOAD_FOLDER = '/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_CONNECTION_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = config.secret
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['RESTX_MASK_SWAGGER'] = False
    app.app_context().push()
    # db1 = flask_sqlalchemy.SQLAlchemy(app)
    # db1.init_app(app)
    return app


app = create_app()
