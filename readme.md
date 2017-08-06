# Data preparation
`$ python ./convert_file.py  ../../data`

# How to Train
Training involes two files: `train.py` and `augmentation/client.py`.

`train.py` will open a local network port waiting for data. 
It trains the AudioNet once it gets a data source.

`client.py` is the data source. It reads wave files and performs data augmentation.

Before training, there are several things you should do.

## data
* gain data for training. 
* split data into two part: train, validate
* put train data into `data/train/`
* put validate data into `data/test/`

## data augmentation
* gain `sox` from [SOund eXchange](https://sourceforge.net/projects/sox/files/sox/14.4.2/), you should get a zip file.
* extract zip file into the `sox` folder. __so that there exists `sox/sox.exe`__.

## How to Run
server side: `$python ./train.py`

client side: `$python ./client.py` (in './augumentation' folder)

## note
If you want to resume from certain checkpoint, modify the last line of `train.py`, change `-1` to your start point.

# Evaluate trained models
run `webfront.py`, start a web server and input URL:http://127.0.0.1:5000/predict. It requires `[ffmpeg](https://ffmpeg.org/)` for format convertion.

## Get FFMPEG
* Download ffmpeg from [ffmpeg](http://ffmpeg.zeranoe.com/builds/), you should select `Static` linking and get a zip file.
* extract the zip file into `ffmpeg` folder, __so that there exists `ffmpeg/bin/ffmeg.exe`__.

## Select Checkpoint for Evaluation
modify `webfront.py`, change `MODEL_ID` to yours.

## How to quickly valid the accuracy of your model?  
*  Run webfront.py! It offer a web UI for uploading a audio file and report the predicted result using your model. 
*  Open a web browser and input URL: http://127.0.0.1:5000/predict. 

`$ python ./webfront.py`

# How to deploy your model? 
*  Convert model file *.h5 to *.pb file 
*  Place your *.pb file where you want to deploy.
*  See Android mobile example: [androidAudioRecg](http://gitlab.icenter.tsinghua.edu.cn/saturnlab/audioNet)

`$ python ./create_pb.py  XX`

