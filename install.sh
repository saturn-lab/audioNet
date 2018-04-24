#!/usr/bin/env bash
ptitle() {
    echo -e "[\033[1;32m$1\033[0;m]"
}

wget http://101.6.160.58/index.php/s/IZ15dN63CRrmfhC/download -O ./data/blueToothWav.zip
apt-get install ffmpeg sox unzip
pip install grpcio grpcio-tools keras

cd data/ && unzip blueToothWav.zip && cd ..
mv data/wav/* data/train/
mv $(ls data/train/* | tail -500) data/test
ptitle "TEST_SIZE" && ls data/test/* | wc -l
ptitle "TRAIN_SIZE" && ls data/train/* | wc -l

mkdir -p ffmpeg/bin
ln -s $(which ffmpeg) ffmpeg/bin/ffmpeg
ln -s $(which sox) sox/sox

ptitle "ffmpeg" && ls ffmpeg/bin/ffmpeg
ptitle "sox" && ls sox/sox

