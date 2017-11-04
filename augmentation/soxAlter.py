#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# Outer Dependency:
#   SOund Exchange, sox.

import os, subprocess
from  random import random, randint
import sys

EF_RATE = 0.6
SOX_PATH = os.path.dirname(os.path.realpath(__file__))
SOX_PATH = os.path.join(SOX_PATH, '..', 'sox', 'sox')

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
        center = randint(1000, 3000)
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
    chain = ' -r 16k -e signed -b 16 -V1 %s  %s'%(filename, outname)
    chain = SOX_PATH + chain
    
    chain += _pitch()
    chain += _tempo()
    chain += _flanger()
    chain += _echo()
    chain += _bandpass()
    chain += _norm()
    
    # execute
    return subprocess.call(chain, shell=True)

def noAlter(filename, outname):
    chain = ' -r 16k -e signed -b 16 -V1 %s %s'%(filename, outname)
    chain = SOX_PATH + chain
    return subprocess.call(chain, shell=True)