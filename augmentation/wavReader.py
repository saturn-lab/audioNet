#!/opt/anaconda3/bin/python

import argparse
import os
import numpy

class Format:
    size=0   # size of this 'fmt ' chunk
    fmtTag=0 
    nChannel=0  # channel number
    sps=0  # samples per second
    bps=0  # bytes per second
    
    def __init__(self, buf):
        self.size = numpy.frombuffer(buf[16:20], dtype=numpy.uint32)[0]
        self.fmtTag = numpy.frombuffer(buf[20:22], dtype=numpy.uint16)[0]
        self.nChannel = numpy.frombuffer(buf[22:24], dtype=numpy.uint16)[0]
        self.sps = numpy.frombuffer(buf[24:28], dtype=numpy.uint32)[0]
        self.bps = numpy.frombuffer(buf[28:32], dtype=numpy.uint32)[0]
    
def _parseData(buf):
    if buf[0:4] != b'RIFF':
        raise ValueError('"RIFF" header is missing')
    if buf[8:12] != b'WAVE':
        raise ValueError('"WAVE" header is missing')
    if buf[12:16] != b'fmt ':
        raise ValueError('"fmt " header is missing')
    fmt = Format(buf)
    itr = 12 + fmt.size + 8
    #print numpy.fromstring(buf[0:50], dtype=numpy.uint8)
    while(itr < len(buf)):
        riffid = buf[itr:itr+4]
        size = numpy.frombuffer(buf[itr+4:itr+8], dtype=numpy.uint32)[0]
        if riffid != b'data':
            itr += 8 + size
        else:
            break
    if riffid != b'data':
        raise ValueError('"data" header is missing')
    data = numpy.frombuffer(buf[itr + 8: itr + 8 + size], dtype=numpy.float32)
    return fmt.sps, data


def readWav(filename):
    with open(filename, 'rb') as f:
        buf = f.read()
        sps, data = _parseData(buf)
    return sps, data  
    # label ,    samples per second,   samples

def parseName(filename): # ./xx/yy/10000_12.wav
    filename = filename.split(os.sep)
    filename = filename[len(filename) - 1]
    filename = filename.split('.')[0]
    filename = filename.split('_')
    filename = filename[len(filename) - 1]
    try:
        label =  int(filename)
    except:
        label = -1
    if(label < 0 or label > 23):
        raise ValueError(filename)
    return label

def numpyToWav(data, fname):
    with open('./template.wav', 'rb') as f:
        template = f.read()
    itr = 12
    while True:
        riffid = template[itr:itr+4]
        if riffid != b'data':
            itr += 4
            itr += numpy.fromstring(template[itr:itr+4], dtype=numpy.uint32)[0]
            itr += 4
        else:
            break
    
    F = numpy.zeros([len(data)*4 + 8 + itr], dtype=numpy.uint8)
    F[0:itr+4] = numpy.fromstring(template[0:itr+4], dtype=numpy.uint8)
    F[4:8] = numpy.fromstring(numpy.array([len(data)*4 + itr - 4], dtype=numpy.uint32).tostring(), dtype=numpy.uint8)
    F[22:24] = numpy.fromstring(numpy.array([1], dtype=numpy.uint16).tostring(), dtype=numpy.uint8)
    F[24:28] = numpy.fromstring(numpy.array([44100], dtype=numpy.uint32).tostring(), dtype=numpy.uint8)
    F[28:32] = numpy.fromstring(numpy.array([44100*4], dtype=numpy.uint32).tostring(), dtype=numpy.uint8)
    F[32:34] = numpy.fromstring(numpy.array([4], dtype=numpy.uint16).tostring(), dtype=numpy.uint8)
    F[34:36] = numpy.fromstring(numpy.array([32], dtype=numpy.uint16).tostring(), dtype=numpy.uint8)
    itr += 4
    F[itr:itr + 4] = numpy.fromstring(numpy.array([len(data)*4], dtype=numpy.uint32).tostring(), dtype=numpy.uint8)
    itr += 4
    print(F.shape - itr)
    print(data.dtype)
    F[itr:] = numpy.fromstring(data.tostring(), dtype=numpy.uint8)
    with open(fname, 'wb') as f:
        f.write(F.tostring())
    return
if __name__ == '__main__':
    #parse = argparse.ArgumentParser()
    #parse.add_argument('input')
    #args = parse.parse_args()
    
    ######  HERE  #######
    import sys
    sps, data = readWav(sys.argv[1])
    ######  HERE  ####### 
    print(sps, len(data))
    print(max(data))
