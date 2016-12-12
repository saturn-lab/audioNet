#!/usr/bin/env python
# -*- coding:utf-8 -*-

import pysox as ps
import os
from  random import random, randint

EF_RATE=0.6

def _pitch(chain):
    if random() < EF_RATE:
        P = str(randint(-500, 500))
        ef = ps.CEffect('pitch', [P])
        chain.add_effect(ef)
        ef = ps.CEffect('rate', ['44100'])
        chain.add_effect(ef)
    return chain

def _tempo(chain):
    if random() < EF_RATE:
        t = str(random() + 0.5)
        ef = ps.CEffect('tempo', [t])
        chain.add_effect(ef)
    return chain

def _flanger(chain):
    if random() < EF_RATE:
        ef = ps.CEffect('flanger', [])
        chain.add_effect(ef)
    return chain

def _echo(chain):
    if random() < EF_RATE:
        gout = str(random()/3 + 0.6)
        dlay = str(randint(50, 200))
        dcay = str(random()/3 + 0.3)
        ef = ps.CEffect('echos', [b'0.98', gout, dlay, dcay])
        chain.add_effect(ef)
    return chain

def _bandpass(chain):
    if random() < EF_RATE:
        center = randint(1000, 5000)
        width = str(randint(center /10, center))
        center = str(center)
        ef = ps.CEffect('bandpass', [center, width])
        chain.add_effect(ef)
    return chain

def _norm(chain):
    dbL = str(randint(-10, 20))
    ef = ps.CEffect('norm', [dbL])
    chain.add_effect(ef)
    return chain

def soxAlter(filename, outname):
    din = ps.CSoxStream(filename)
    
    encoding = ps.CEncodingInfo(ps.CEncodingInfo.FLOAT, 32)
    signal = ps.CSignalInfo(44100, 1)
    #outname = './tmp/' + str(getpid()) + '.wav'

    out = ps.CSoxStream(outname, 'w', signal, encoding, 'wav')

    chain = ps.CEffectsChain(din, out)
    
    # 通道归一，必须，否则会对rate造成不必要的影响
    ef = ps.CEffect('channels', [b'1'])
    chain.add_effect(ef)
    
    _pitch(chain)
    _tempo(chain)
    _flanger(chain)
    _echo(chain)
    _bandpass(chain)
    _norm(chain)

    chain.flow_effects()
    

    out.close()

if __name__ == '__main__':
    os.system('rm ./tmp/*')
    soxAlter('/home/saturn/ds/data2/bluetooth/total/0001/a.mp3')
