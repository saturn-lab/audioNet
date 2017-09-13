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

## Step 1.4 Install Grpc
The data augmentation server is implemented by grpc.

`$ pip install grpcio`

or for some version of python3

`$ pip3 install grpcio`

# Step 2. How to train a deep model?
Training involes two files: `train.py` and `augmentation/`.

`$ python -m augmentation` will start a augmentation server that provide train data and test data.
`train.py` will connect to augmentation server and request data.

`augmentation/config.py` is used for configuring the batch size/thread size/data source/...

Before training, there are several things you should do.

## Step 2.1 data placement.
* convert raw audio files to uniformed *.wave files for training. 
* split data into two part: train, validate
* put train data into `data/train/`
* put validate data into `data/test/`
* NOTE: the wav file must be encoded by 16 bit signed integer, mono-channeled and at a sampling rate of 16000.
* see [audioPlot](htttp://gitlab.icenter.tsinghua.edu.cn/saturnlab/audioPlot) for converting tools.
## step 2.2 data augmentation.
* gain `sox` from [SOund eXchange](https://sourceforge.net/projects/sox/files/sox/14.4.2/), you should get a zip file.
* extract zip file into the `sox` folder. __so that there exists `sox/sox.exe`__.

## Step 2.3 How to Run training process?
server side: `$python -m augmentation`
client side: `$python train.py`

* NOTE: run it from the folder `audioNet`

** Resume a interrupted training process.
You can resume from certain checkpoint, modify the last line of `train.py`, change `-1` to your start point.

# Step 3. Evaluate a trained models
## Step 3.1 Select Checkpoint for Evaluation
modify `webfront.py`, change `MODEL_ID` to yours.

## Step 3.2 Run `python webfront.py`. 
open a web browser and input URL:http://127.0.0.1:5000/predict. 

## Step 3.3 You can record a voice directive and upload it for test immediately. 

*It requires `[ffmpeg](https://ffmpeg.org/)` for audio file format convertion.

** Select Checkpoint for Evaluation
modify `webfront.py`, change `MODEL_ID` to yours.

# Step 4. How to deploy your model in Web Server?   
*  Modify webfront.py, change "MODEL_ID=XX".
*  start a web server andand input URL: http://127.0.0.1:5000/predict. 

`$ python ./webfront.py`

# Step 5. How to deploy your model in mobile? 
*  Convert model file *.h5 to *.pb file 
*  Place your *.pb file where you want to deploy.
*  See Android mobile example: [androidAudioRecg](http://gitlab.icenter.tsinghua.edu.cn/saturnlab/androidAudioRecg)

`$ python ./create_pb.py  XX`

