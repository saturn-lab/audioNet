# Step 1. Tools preparation
## Step 1.1 Get FFMPEG
* Download ffmpeg from [ffmpeg](http://ffmpeg.zeranoe.com/builds/), you should select `Static` linking and get a zip file.
* extract the zip file into `ffmpeg` folder, __so that there exists `ffmpeg/bin/ffmeg.exe`__.

## Step 1.2 Get SOX
* Download sox from [SOund eXchange](https://sourceforge.net/projects/sox/files/sox/14.4.2/), you should get a zip file.
* extract zip file into the sox folder. so that there exists `sox/sox.exe`.

## Step 1.3 Data preparation
Convert recorded audio files to *.wav files

`$ python ./convert_file.py  <Data Folder>`

The `Data Folder` should contains many subfolders where your audios files reside. Typically, one of your audio file could be `<Data Folder>/group1/0001.mp3`.

The results of conversion are within `./data/train/`. Your should manually move some of them to `./data/test` to accomplish `training-validation` separation. 
The fraction of moved files depends on yourself.

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
You have done it in `Data preparation`. Now check it again.

* put train data into `data/train/`
* put validate data into `data/test/`

* NOTE: the wav file must be encoded by 16 bit signed integer, mono-channeled and at a sampling rate of 16000.
* You should got things correct if you obtained them from `convert_file.py`

## step 2.2 data augmentation.
* You should got sox in `sox/`, now check it again.

## Step 2.3 How to Run training process?
server side: `$python -m augmentation`
* this will start an augmentation server utilizing `sox`.

client side: `$python train.py`
* this will start trainig with data requested from augmentation server.

* NOTE: run it from the folder `audioNet`

** Resume a interrupted training process.
You can resume from certain checkpoint, modify the last line of `train.py`, set `-1`(Negtive 1) as your start point.

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
See `Run python webfront.py`

# Step 5. How to deploy your model in mobile? 
* Choose an `ID` of checkpoint by yourself from `models/save_<ID>.h5`.
* Run `$ python ./create_pb.py  <ID>`.  This will create file `models/model.pb`
*  Place your model.pb file where you want to deploy. Typically, see Android mobile example: [androidAudioRecg](http://gitlab.icenter.tsinghua.edu.cn/saturnlab/androidAudioRecg)


