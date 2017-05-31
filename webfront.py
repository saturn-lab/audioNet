#!/opt/anaconda3/bin/python
# -*- coding:utf-8 -*-

import os, sys, subprocess
from flask import Flask, request, redirect, flash
from werkzeug.utils import secure_filename
import numpy

sys.path.append('augmentation' + os.sep)

from wavReader import readWav
from model import KerasModel

UPLOAD_FOLDER = '.' + os.sep + 'tmp'
FFMPEG_PATH='.' + os.sep + 'ffmpeg' + os.sep + 'bin' + os.sep + 'ffmpeg'

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

DICT=[
    '蓝牙开机',
    '蓝牙拨打电话',
    '蓝牙打电话',
    '蓝牙接听电话',
    '蓝牙接电话',
    '蓝牙拒接',
    '蓝牙播放音乐',
    '蓝牙开始音乐',
    '蓝牙暂停音乐',
    '蓝牙停止音乐',
    '蓝牙上一首',
    '蓝牙上一曲',
    '蓝牙下一首',
    '蓝牙下一曲',
    '蓝牙音量增大',
    '蓝牙声音增大',
    '蓝牙音量增加',
    '蓝牙声音增加',
    '蓝牙音量减小',
    '蓝牙声音减小',
    '蓝牙关机',
    '蓝牙电量提醒',
    '蓝牙还剩多少电',
    '蓝牙还剩多少电量'
    ]

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
        if file :#and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            fullpath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            if os.path.exists(fullpath) and os.path.isfile(fullpath):
                os.remove(fullpath)
            file.save(fullpath)  # save the uploaded file
            
            if os.path.exists(FFMPEG_PATH) or os.path.exists(FFMPEG_PATH + '.exe'):
                ffmpeg_cmd = ' -i {} -ac 1 -acodec pcm_f32le -ar 11025 {}.wav -v 1'.format(fullpath, fullpath)
                ffmpeg_cmd = FFMPEG_PATH + ffmpeg_cmd
                
                os.system(ffmpeg_cmd)
                res = predict(fullpath + '.wav', '.' + os.sep + 'models' + os.sep + 'save_05.h5')
            else:
                flash('Unable to find ffmpeg, please install ffmpeg')
                return redirect(request.url)

            return str(DICT[res])

    return '''
    <!doctype html>
    <title>audioNet Predict</title>
    <h1>Upload audio for predict</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file accept='audio/*' capture>
         <input type=submit value=Upload>
    </form>
    '''

if __name__ == "__main__" :
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(host='0.0.0.0', port=5000)
