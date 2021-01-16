import os
from flask import Flask, flash, request, redirect, url_for, render_template, send_file
from werkzeug.utils import secure_filename

os.chdir(os.path.dirname(os.path.abspath(__file__)))

UPLOAD_FOLDER = 'tempUploads/'
PROCESSED_FILES_FOLDER = 'processedUploads/'
PATH_OF_KINKADE_TRANSFER_LEARNING_APP = '../KinkadeCMDBuild/KinkadeCMD'

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 5 * 1000 * 1000 # Specifies rough max size of upload in mb.

def verify_file(file: str):
    if file != "" and "." in file and file.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS:
        filename = secure_filename(file)
        return filename
    return None

def process_image(verified_file, file):
    # Download file from user.
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], verified_file)
    if os.path.exists(file_path): os.remove(file_path)
    file.save(file_path)

    # Process file.
    out_path = os.path.join(PROCESSED_FILES_FOLDER, verified_file)
    if os.path.exists(out_path): os.remove(out_path)
    os.system(PATH_OF_KINKADE_TRANSFER_LEARNING_APP + " \"" + file_path + "\"" + " \"" + out_path + "\"")
    
    if os.path.exists(out_path):
        return out_path
    else:
        return ""

@app.route('/kinkade_file', methods = ['GET'])
def kinkade_file():
    return "SUCCESS!"

@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == "POST":
        # If a file is not provided give error screen.
        if 'file' not in request.files:
            return redirect(url_for('index', invalid_upload = True))

        # Fetch file and provide error if its non-existant.
        file = request.files['file']
        verified_file = verify_file(file.filename)
        if verified_file == None:
            return redirect(url_for('index', invalid_upload = True))
        
        # Process image and send invalid message if something is wrong.
        file_path = process_image(verified_file, file)
        if file_path == "":
            print ("Error: Something went wrong with processing of file.")
            return redirect(url_for('index', invalid_upload = True))
        return send_file(file_path)
    
    else:
        # Is a valid upload by default
        invalid_upload = False
        if "invalid_upload" in request.args:
            invalid_upload = True
        return render_template('index.html', invalid_upload = invalid_upload)
    

if __name__ == "__main__":
    app.run()
        

