from flask import render_template, request, jsonify, Flask
import os
import glob
import json
import json_to_df as jd
import pandas as pd
import os
from celery import Celery

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Configure Celery
def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)
    return celery

app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379/0',
    CELERY_RESULT_BACKEND='redis://localhost:6379/0'
)

celery = make_celery(app)

@app.route("/")
def index():
    """Renders first page of application"""
    return render_template("base.html")

@app.route('/upload-files', methods=['POST'])
def upload_files():
    current_directory = '.'
    specific_folder = 'uploads'  # Replace with your folder name
    def remove_files_in_directory(directory):
        files = os.listdir(directory)
        for file in files:
            file_path = os.path.join(directory, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
    remove_files_in_directory(specific_folder)
    if 'files' not in request.files:
        return jsonify({'message': 'No files part in the request'}), 400

    files = request.files.getlist('files')
    filenames = []

    for file in files:
        if file.filename == '':
            return jsonify({'message': 'No selected file'}), 400
        filename = file.filename
        file_path = os.path.join(UPLOAD_FOLDER, filename)

        # Stream the file to the server
        with open(file_path, 'wb') as f:
            for chunk in file.stream:
                f.write(chunk)

        filenames.append(filename)

    print('Received filenames:', filenames)
    return jsonify({'message': 'Files uploaded successfully', 'filenames': filenames})

@app.route('/viewer')
def next_page():
    filenames = os.listdir(UPLOAD_FOLDER)
    print('Filenames on next page:', filenames)
    path = './uploads'
    tables = {}
    meta = {}

    for filename in filenames:
        print(filename)
        if filename.split('.')[-1] == 'ndjson':
            json_data = jd.ndjson_conversion(path+'/'+filename)
        else:
            with open(path+'/'+filename, 'r', encoding='iso-8859-1') as f:
                json_data = json.load(f)
        xdf = jd.create_xpt(json_data)
        meta_dict = {'itemOID':[],'name':[],'label':[],'dataType':[],'targetDataType':[],'displayFormat':[],'length':[],'keySequence':[]}
        col_info = json_data['columns']
        for i in range(len(col_info)):
            for k in meta_dict.keys():
                if k in col_info[i]:
                    meta_dict[k].append(col_info[i][k])
                else:
                    meta_dict[k].append('')
        meta_df = pd.DataFrame(meta_dict)
        meta_html = meta_df.to_html(classes='metadata',header='true',index=False)
        meta[filename] = meta_html
        table_html = xdf.to_html(classes='data', header="true", index=False)
        tables[filename] = table_html

    return render_template('viewer.html', filenames=filenames, tables=tables, meta=meta, json_data=json_data)

@app.route('/process-file/<filename>')
def process_file(filename):
    process_file_task.delay(filename)
    return jsonify({'message': 'File processing started'}), 202


@app.route('/go-back-to-base', methods=['POST'])
def go_back_to_base():
    # Delete files from the folder
    folder_path = 'uploads/'
    files = glob.glob(os.path.join(folder_path, '*'))
    for f in files:
        os.remove(f)
    # Render the base.html template
    return render_template('base.html')

@app.route('/home')
def home():
    return redirect(url_for('index'))

@celery.task
def process_file_task(filename):
    # Your file processing logic here
    pass

if __name__ == "__main__":
    app.run(debug=False)