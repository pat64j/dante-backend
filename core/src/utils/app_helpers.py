import os, secrets
from flask import current_app as app
from flask import url_for
from werkzeug.utils import secure_filename

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def save_picture(form_picture):
    filename = secure_filename(form_picture.filename)
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(filename)
    picture_fn = random_hex + f_ext
    form_picture.save(os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], picture_fn))
    f_url = url_for('static',filename="avatars/"+picture_fn)

    return f_url