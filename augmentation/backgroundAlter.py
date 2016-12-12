#!/usr/bin/env python

import numpy
import glob
import  random 
from wavReader import readWav, numpyToWav


ALTER_RATE=1.0
RANDOM_GAIN=0.6
BGM_GAIN=0.9
def _getBgn(globstring='./bgn/*.wav'):
    flist = glob.glob(globstring)
    i = random.randint(0, len(flist) - 1)
    f = flist[i]
    _, data = readWav(f)
    return data

def _uniformAlter(data):
    if random.random() < ALTER_RATE:
        noise = numpy.random.random(data.shape)
        noise = numpy.array(noise, dtype=numpy.float32)
        noise = noise - 0.5
        alpha = random.random() * RANDOM_GAIN
        data = (1-alpha) * data + alpha * noise
    return data

def _sytheticAlter(data):
    if random.random() < ALTER_RATE:
        noise = _getBgn()
        alpha = random.random() * BGM_GAIN
        if len(noise) < len(data):
            start = random.randint(0, len(data) - len(noise))
            data = (1 - alpha) * data[start:start + len(noise)] + alpha * noise
        else:
            start = random.randint(0, len(noise) - len(data))
            data = (1- alpha) * data + alpha * noise[start:start + len(data)]
    return data

def bgnAlter(data):
    data = _uniformAlter(data)
    data = _sytheticAlter(data)
    return data

if __name__ == '__main__':
    spl, wav = readWav('./test.wav')
    wav = bgnAlter(wav)
    numpyToWav(wav, './noise.wav')
