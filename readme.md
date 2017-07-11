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

## augmentation
* gain `sox` from [SOund eXchange](https://sourceforge.net/projects/sox/files/sox/14.4.2/), you should get a zip file.
* extract zip file into the `sox` folder. __so that there exists `sox/sox.exe`__.

## How to Run
server side: `$ ./train.py`
client side: `$ ./client.py train`

## note
If you want to resume from certain checkpoint, modify the last line of `train.py`, change `-1` to your start point.

# How to Evaluate
run `webfront.py` it will start a web server, which requires `[ffmpeg](https://ffmpeg.org/)` for format convertion.

## Get FFMPEG
* Download ffmpeg from [ffmpeg](http://ffmpeg.zeranoe.com/builds/), you should select `Static` linking and get a zip file.
* extract the zip file into `ffmpeg` folder, __so that there exists `ffmpeg/bin/ffmeg.exe`__.

## Select Checkpoint for Evaluation
modify `webfront.py`, change `MODEL_ID` to yours.

## How to Run
`$ ./webfront.py`

