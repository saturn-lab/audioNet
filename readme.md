# How to Train
Training involes two file: `train.py` and `augmentation/client.py`.

`train.py` will open a local network port waiting for data. 
It trains the AudioNet as long as it get a data source.

`client.py` is the data source. It reads wave files and performs data augmentation.

## codes
serer side: `$ ./train.py`

train-data client side: `$ ./client.py train`
test-data client side: `$ ./client.py test`

server side need both train-data and test-data to proceed.

## note
parameters like file path should be modified manual in `train.py` and `client.py`.

# How to Evaluate
run `webfront.py` it will start a web server, which requires `ffmpeg` for format convertion.

it uses the saved model for prediction. the model-path is set in the file. 

modification is usually required.