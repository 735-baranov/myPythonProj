#!/usr/bin python3
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_uploads import UploadSet, ALL, configure_uploads
from werkzeug.utils import secure_filename
import os
import zipfile
import shutil
import numpy as np
import glob

from test_sample import make_dataset as md

import kerasik

UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = set(['zip'])

files = UploadSet('files', ALL)
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# bootstrap = Bootstrap(app)

def al_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/avtor', methods=['GET', 'POST'])
def avtor_def():
    return render_template('avtor.html')


@app.route('/tone', methods=['GET', 'POST'])
def tone_def():
    return render_template('tone.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and al_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            zip_ref = zipfile.ZipFile(UPLOAD_FOLDER + filename, 'r')
            zip_ref.extractall(UPLOAD_FOLDER)
            zip_ref.close()
            os.remove(UPLOAD_FOLDER + filename)

            temp = UPLOAD_FOLDER + os.listdir(UPLOAD_FOLDER)[0]

            return jsonify({'data': '', 'labels': ''})

#
@app.route('/get_data', methods=['GET', 'POST'])
def get_data():
    # if request.method == 'POST':
    num_of_auth = request.form['n_na']
    num_of_files = request.form['n_nf']
    num_of_symb = request.form['n_ns']

    n_rep = request.form['n_rep']
    n_epo = request.form['n_epo']
    n_fol = request.form['n_fol']

    print(num_of_auth, num_of_files, num_of_symb, n_rep, n_epo, n_fol)

    labels, test_files = md(autors=num_of_auth, files=num_of_files, symbols=num_of_symb)

    shutil.rmtree(UPLOAD_FOLDER)

    if not os.path.exists(UPLOAD_FOLDER):
        os.mkdir(UPLOAD_FOLDER)

    kerasik.main(repeats=n_rep, epochs=n_epo, folds=n_fol)

    test_models = glob.glob('testModel*')
    last_model = len(test_models)

    predits_list = glob.glob('test*.csv')
    predits = kerasik.predict(modelfile=test_models[last_model - 1], validata=predits_list[0], outfile='predict.csv')
    data = np.array(predits).tolist()[0]

    #
    # predits_list = glob.glob('test*.csv')
    # predits_data = []
    # for pl in predits_list:
    #     predits = kerasik.predict(modelfile=test_models[last_model-1], validata=pl, outfile='predict.csv')
    #     predits_data.append(np.array(predits).tolist()[0])
    #
    # print(predits_data[0][1])

    # clear_block
    del_csv = glob.glob('*.csv')
    for f in del_csv:
        os.remove(f)

    del_json = glob.glob('*.json')
    for fj in del_json:
        os.remove(fj)

    del_mod = glob.glob('testModel*')
    for fm in del_mod:
        os.remove(fm)

    # data = [1, 2, 4, 4, 65, 4]

    return jsonify({'data': data, 'labels':labels})

@app.route('/data')
def get_begining():
    labels = ['1', '2', '3', '4', '5']
    data = [5, 4, 3, 2, 1]
    return jsonify({'data': data, 'labels': labels})


if __name__ == '__main__':

    if not os.path.exists(UPLOAD_FOLDER):
        os.mkdir(UPLOAD_FOLDER)

    app.run(host='localhost', port='5000', debug=False)


