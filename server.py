import os
from flask import Flask, flash, request, redirect, url_for
from flask import send_from_directory
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './SharedFiles'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.add_url_rule(
    "/uploads/<name>", endpoint="download_file", build_only=True
)


def allowed_files(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        files = request.files.getlist('files')
        print(f"the files are {files}")

        if not files:
            flash('No selected file')
            return redirect(request.url)

        for file in files:
            if file and allowed_files(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        return redirect(url_for('download_file', name=files[-1].filename))


@app.route('/uploads/')
def view_uploads():
    return os.listdir(app.config['UPLOAD_FOLDER'])


@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)


@app.route('/uploads/<name>', methods=['DELETE'])
def delete_file(name):
    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], name))
    return {"result": "awesomepossum"}
