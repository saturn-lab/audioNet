#!/usr/bin/env python2

import os, sys, subprocess
from flask import Flask, request, redirect, flash
from werkzeug.utils import secure_filename
import numpy

sys.path.append('./augmentation/')

from wavReader import readWav
from model import KerasModel

UPLOAD_FOLDER = '/tmp/audioNet'
ALLOWED_EXTENSIONS = set(['wav', 'mp3', 'wma', 'aac'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def predict(wavfile, modelfile):
    spl, wav = readWav(wavfile)
    wav = wav.reshape([1, -1, 1, 1])

    modelA = KerasModel()
    modelA.load_weights(modelfile)

    result = modelA.predict(wav, 1)
    return numpy.argmax(result, 1)

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def command_exists(command):
    return subprocess.call('type ' + command, shell=True, 
        stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0

@app.route('/predict', methods=['GET', 'POST'])
def predictAction():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            fullpath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(fullpath)  # save the uploaded file
            # check if file is wav
            if filename.rsplit('.', 1)[1] != 'wav':
                if command_exists('ffmpeg'):
                    ffmpeg_cmd = 'ffmpeg -i {} -ac 1 -acodec pcm_f32le -ar 44100 {}.wav -v 1'.format(fullpath, fullpath)
                    os.system(ffmpeg_cmd)
                    res = predict(fullpath + '.wav', '/home/ubuntu/audioNet/models/save_14.h5')
                else:
                    flash('Unable to find ffmpeg, please install ffmpeg')
                    return redirect(request.url)
            else:
                # run predict
                res = predict(fullpath, '/home/ubuntu/audioNet/models/save_14.h5')
            return str(res)

    return '''
    <!doctype html>
    <title>audioNet Predict</title>
    <h1>Upload audio for predict</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

if __name__ == "__main__" :
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(host='0.0.0.0')
