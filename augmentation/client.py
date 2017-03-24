#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import socket
import numpy
import time
import glob
import os
import sys
from random import randint

from wavReader import readWav, parseName

from backgroundAlter import bgnAlter

import queue
import threading

TRAIN_DATA_DIR='..' + os.sep + 'data' + os.sep + 'train'
TEST_DATA_DIR = '..' + os.sep + 'data' + os.sep + 'test'


# è¯»å–æ•°æ®ï¼Œæ”¾å…¥é˜Ÿåˆ—çš„çš„çº¿ç¨‹å‡½æ•°
def _enQueueData(dpath, alter, Q):
    flist = glob.glob(dpath) 
    outf = '.' + os.sep + 'tmp' + os.sep + str(os.getpid()) + '.wav'
    thrd = threading.currentThread()
    while getattr(thrd, 'running', True):
        f = flist[randint(0, len(flist) - 1)]
        label = parseName(f)
        if alter:
            # Alter file 'f' to 'outf' for file-level transform
            sps, data = readWav(f)
            bgnAlter(data)
            # in-memory transform
        else:
            sps, data = readWav(f)
        data = data[1:] - data[0:len(data) - 1] # Z å˜æ¢
        Q.put((label, data), True)

# åˆ›å»ºçº¿ç¨‹ï¼Œè¿”å›žçº¿ç¨‹å’Œé˜Ÿåˆ—
def _dataThreadOn(dpath, alter=True, maxQ=128):
    Q = queue.Queue(maxQ)
    thrd = threading.Thread(target=_enQueueData, args = (dpath, alter, Q))
    thrd.start()
    return thrd, Q

# å‘é€æ‰€æœ‰æ•°æ®ï¼Œé˜»å¡žæ¨¡å¼
def _sendall(s, data):
    length = len(data)
    minimal = 512
    prog = 0
    prog += s.send(data[0:8])
    while prog < length:
        prog += s.send(data[8:len(data)])
    return None

# ä¸»è¦å‡½æ•°ï¼Œåˆ›å»ºä¸€ä¸ªsocketï¼Œå‘sock_addrå‘é€æ•°æ®ï¼Œå¹¶ä¸”è´Ÿè´£IOçº¿ç¨‹çš„ç®¡ç†
def startAlterShipping(port, glob_string, alter=True):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', port))

    thrd, Q = _dataThreadOn(glob_string, alter=alter, maxQ=64)
    
    try:
        while True :
            label, data = Q.get()
            label = numpy.array([label, data.shape[0]], dtype=numpy.uint32)
            e = _sendall(s, label.tostring() + data.tostring())
            print('data over')
            Q.task_done()
    except:
        print('Out')
        s.close()
        thrd.running = False
        _, _ = Q.get()
        Q.task_done()
        threading.Thread.join(thrd)

if __name__ == '__main__':
    t = sys.argv[1]
    if t == 'train':
        print('train')
        startAlterShipping(9009, TRAIN_DATA_DIR + os.sep + '*.wav')
    else:
        print('test')
        startAlterShipping(9090, TEST_DATA_DIR + os.sep + '*.wav')
    
