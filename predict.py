#!/usr/bin/env python
import sys
import numpy

sys.path.append('./augmentation/')

from wavReader import readWav
from model import KerasModel


def predict(wavfile, modelfile):
    spl, wav = readWav(wavfile)
    wav = wav.reshape([1, -1, 1, 1])
    
    modelA = KerasModel()
    modelA.load_weights(modelfile)

    return modelA.predict(wav, 1)
if __name__ == '__main__':
    a = predict('./augmentation/template.wav', './models/save_14.h5')
    print numpy.argmax(a, 1)
