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


def get_file_names():
    list_of_files_as_li = ""
    for file in os.listdir(app.config['UPLOAD_FOLDER']):
        list_of_files_as_li += f"""<li> {file} 
        <a href="{url_for('download_file', name=file)}">
            <button> Download </button>
        </a>
        </li>"""
    return f"<ul>{list_of_files_as_li}</ul>"


def allowed_files(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    current_working_directory = os.getcwd()
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_files(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('download_file', name=filename))
    return f'''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File to {current_working_directory + UPLOAD_FOLDER}</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    {get_file_names()}

    '''

@app.route('/uploads/')
def view_uploads():
    return os.listdir(app.config['UPLOAD_FOLDER'])

@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)
@app.route('/uploads/<name>', methods=['DELETE'])
def delete_file(name):
    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], name))


@app.route('/test')
def test():
    return {"data": "test"}