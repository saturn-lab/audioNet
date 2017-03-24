#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import os
from  random import random, randint
import sys

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
    chain = 'sox %s -c 1 -r 11025 -b 16 %s'%(filename, outname)

    chain += _pitch()
    chain += _tempo()
    chain += _flanger()
    chain += _echo()
    chain += _bandpass()
    chain += _norm()

    # execute
    return os.system(chain)

if __name__ == '__main__':
    os.system('rm ./tmp/*')
    if len(sys.argv) < 2:
        din = '/home/saturn/ds/data2/bluetooth/train/raw/2003880056/k.mp3'
    else:
        din = sys.argv[1]
    soxAlter(din, './test.wav')
