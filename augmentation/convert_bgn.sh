#!/bin/sh
filesin=`find $1 -name '*.*'`

for arg in $filesin
do
    if [ -f $arg ]
    then
        name=`basename $arg`
        ffmpeg -i $arg -ac 1 -acodec pcm_f32le -ar 44100 $1/tmp_$name.wav -v 1
        sox $1/tmp_$name.wav $1/norm_$name.wav norm -n
        rm $arg $1/tmp_$name.wav
    fi
done
