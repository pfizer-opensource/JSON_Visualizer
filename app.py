from flask import render_template, request, jsonify, Flask, send_file
import os
import glob
import json
import json_to_df as jd
import pandas as pd
import io

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
DATA_FOLDER = 'data'
METADATA_FOLDER = "metadata"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DATA_FOLDER, exist_ok=True)
os.makedirs(METADATA_FOLDER, exist_ok=True)


@app.route("/")
def index():
    """Renders first page of application"""
    return render_template("base.html")

@app.route('/upload-files', methods=['POST'])
def upload_files():
    specific_folder = ['uploads','data','metadata']
    def remove_files_in_directory(directory):
        files = os.listdir(directory)
        for file in files:
            file_path = os.path.join(directory, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
    for folder in specific_folder:
        remove_files_in_directory(folder)
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
    json_data = {}

    for filename in filenames:
        print(filename)
        if filename.split('.')[-1] == 'ndjson':
            json_data[filename] = jd.ndjson_conversion(path+'/'+filename)
        else:
            with open(path+'/'+filename, 'r', encoding='iso-8859-1') as f:
                json_data[filename] = json.load(f)
        xdf = jd.create_xpt(json_data[filename])
        meta_dict = {'itemOID':[],'name':[],'label':[],'dataType':[],'targetDataType':[],'displayFormat':[],'length':[],'keySequence':[]}
        col_info = json_data[filename]['columns']
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

        modified_filename = filename.replace('.', '_')
        data_excel_path = os.path.join(DATA_FOLDER, f"{modified_filename}_data.xlsx")
        meta_excel_path = os.path.join(METADATA_FOLDER, f"{modified_filename}_metadata.xlsx")
        xdf.to_excel(data_excel_path, index=False)
        meta_df.to_excel(meta_excel_path, index=False)


    return render_template('viewer.html', filenames=filenames, tables=tables, meta=meta, json_data=json_data)

@app.route('/process-file/<filename>')
def process_file(filename):
    process_file_task.delay(filename)
    return jsonify({'message': 'File processing started'}), 202


@app.route('/download_current', methods=['POST'])
def download_current():
    data = request.get_json()
    filename = data.get('filename')
    print(filename)
    table_type = data.get('type')
    print(table_type)

    app.logger.info(f"Received request for filename: {filename}, type: {table_type}")

    if not filename or not table_type:
        return jsonify({'message': 'Invalid request'}), 400

    if table_type == 'metadata':
        folder = METADATA_FOLDER
    else:
        folder = DATA_FOLDER

    file_path = os.path.join(folder, f"{filename.replace('.', '_')}_{table_type}.xlsx")

    app.logger.info(f"Constructed file path: {file_path}")

    if not os.path.exists(file_path):
        app.logger.error(f"File not found: {file_path}")
        return jsonify({'message': 'File not found'}), 404

    return send_file(file_path, download_name=f"{filename}_{table_type}.xlsx", as_attachment=True)

@app.route('/download_all', methods=['POST'])
def download_all():
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')

    for folder, table_type in [(DATA_FOLDER, 'data'), (METADATA_FOLDER, 'metadata')]:
        for file in os.listdir(folder):
            if file.endswith('.xlsx'):
                sheet_name = file.replace(f"_{table_type}.xlsx", "").replace('_', '.')
                df = pd.read_excel(os.path.join(folder, file))
                df.to_excel(writer, sheet_name=f"{sheet_name}_{table_type}", index=False)

    writer.close()
    output.seek(0)

    return send_file(output, download_name='all_tables.xlsx', as_attachment=True)

@app.route('/go-back-to-base', methods=['POST'])
def go_back_to_base():
    folder_path = ['uploads/','data/','metadata/']
    for folder in folder_path:
        files = glob.glob(os.path.join(folder, '*'))
        for f in files:
            os.remove(f)
    return render_template('base.html')

@app.route('/home')
def home():
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=False)