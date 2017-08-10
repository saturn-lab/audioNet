# Step 1. Tools preparation
## Step 1.1 Get FFMPEG
* Download ffmpeg from [ffmpeg](http://ffmpeg.zeranoe.com/builds/), you should select `Static` linking and get a zip file.
* extract the zip file into `ffmpeg` folder, __so that there exists `ffmpeg/bin/ffmeg.exe`__.

## Step 1.2 Get SOX
* Download sox from SOund eXchange, you should get a zip file.
* extract zip file into the sox folder. so that there exists sox/sox.exe.

## Step 1.3 Data preparation
Convert recorded audio files to *.wav files

`$ python ./convert_file.py  ../../data`

# Step 2. How to train a deep model?
Training involes two files: `train.py` and `augmentation/client.py`.

`train.py` will open a local network port waiting for data. 
It trains the AudioNet once it gets a data source.

`client.py` is the data source. It reads wave files and performs data augmentation.

Before training, there are several things you should do.

## Step 2.1 data placement.
* convert raw audio files to uniformed *.wave files for training. 
* split data into two part: train, validate
* put train data into `data/train/`
* put validate data into `data/test/`

## step 2.2 data augmentation.
* gain `sox` from [SOund eXchange](https://sourceforge.net/projects/sox/files/sox/14.4.2/), you should get a zip file.
* extract zip file into the `sox` folder. __so that there exists `sox/sox.exe`__.

## Step 2.3 How to Run training process?
server side: `$python ./train.py`

client side: `$python ./client.py` (in './augumentation' folder)

## Resume a interrupted training process.
You can resume from certain checkpoint, modify the last line of `train.py`, change `-1` to your start point.

# Step 3. Evaluate a trained models
## Select Checkpoint for Evaluation
modify `webfront.py`, change `MODEL_ID` to yours.

##Run `python webfront.py`. 
open a web browser and input URL:http://127.0.0.1:5000/predict. 

##You can record a voice directive and upload it for test immediately. 

*It requires `[ffmpeg](https://ffmpeg.org/)` for audio file format convertion.

## Select Checkpoint for Evaluation
modify `webfront.py`, change `MODEL_ID` to yours.

# Step 4. How to deploy your model in Web Server?   
*  Modify webfront.py, change "MODEL_ID=XX".
*  start a web server andand input URL: http://127.0.0.1:5000/predict. 

`$ python ./webfront.py`

# Step 5. How to deploy your model in mobile? 
*  Convert model file *.h5 to *.pb file 
*  Place your *.pb file where you want to deploy.
*  See Android mobile example: [androidAudioRecg](http://gitlab.icenter.tsinghua.edu.cn/saturnlab/audioNet)

`$ python ./create_pb.py  XX`

