from .. import ALLOWED_EXTENSIONS, app
import os
from flask import send_from_directory
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_file(user_id):
    if 'file' not in request.files:
        return '1'
    file = request.files['file']
    if file.filename == '':
        return '2'
    if file and allowed_file(file.filename):
        file_upd = user_id
        filename = secure_filename(file_upd) + "." + file.filename.rsplit('.', 1)[1].lower()
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return 'True'

def download_profilepic(id):
    for ext in ALLOWED_EXTENSIONS:
        if os.path.isfile(app.config["UPLOAD_FOLDER"] + id + "." + ext):
            return send_from_directory(app.config["UPLOAD_FOLDER"], id + "." + ext)
    return None
