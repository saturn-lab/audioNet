#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import os
from  random import random, randint
import sys

EF_RATE=0.6
SOX_PATH='..' + os.sep + 'sox' + os.sep + 'sox'

def _pitch():
    chain = ' '
    if random() < EF_RATE:
        P = str(randint(-500, 500))
        chain += 'pitch ' + P
    return chain

def _tempo():
    chain = ' '
    if random() < EF_RATE:
        t = str(random() + 0.5)
        chain += 'tempo ' + t 
    return chain

def _flanger():
    chain = ' '
    if random() < EF_RATE:
        chain += 'flanger '
    return chain

def _echo():
    chain = ' '
    if random() < EF_RATE:
        gout = str(random()/3 + 0.6)
        dlay = str(randint(50, 200))
        dcay = str(random()/3 + 0.3)
        chain += 'echos 0.98 %s %s %s'%(gout, dlay, dcay)
    return chain

def _bandpass():
    chain = ' '
    if random() < EF_RATE:
        center = randint(1000, 5000)
        width = str(randint(center // 10, center))
        center = str(center)
        chain += 'bandpass %s %s'%(center, width)
    return chain

def _norm():
    chain = ' '
    dbL = str(randint(-10, 20))
    chain += 'norm %s'%dbL
    return chain

def soxAlter(filename, outname):
    chain = ' %s -c 1 -r 11025 -b 32 %s'%(filename, outname)
    chain = SOX_PATH + chain
    
    chain += _pitch()
    chain += _tempo()
    chain += _flanger()
    chain += _echo()
    chain += _bandpass()
    chain += _norm()
    
    # execute
    return os.system(chain)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        din = '/home/saturn/storage/dataD/bluetooth/train/raw/2003880056/k.mp3'
    else:
        din = sys.argv[1]
    soxAlter(din, './test.wav')
