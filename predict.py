#!/opt/anaconda3/bin/python
import sys
import numpy

sys.path.append('./augmentation/')

from wavReader import readWav
from model import KerasModel
from sockDataGenerator import sockDataGeneratorOrigin

def startPredict(modelfile):
    spl, wav = readWav(wavfile)
    wav = wav.reshape([1, -1, 1, 1])
    
    dg = sockDataGeneratorOrigin('./pred.sock')
    
    modelA = KerasModel(False)
    modelA.load_weights(modelfile)
    
    while True:
        lb, wav, r = dg.next()
        plb = modelA.predict(wav, 1)
        plb = numpy.argmax(plb, 1)
        r.sendall(plb.tostring())

if __name__ == '__main__':
    startPredict('./models/save_14.h5')
