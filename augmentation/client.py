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
from soxAlter import soxAlter

import queue
import threading
import multiprocessing

TRAIN_DATA_DIR='..' + os.sep + 'data' + os.sep + 'train'
TEST_DATA_DIR = '..' + os.sep + 'data' + os.sep + 'test'



# 读取数据，放入队列的的线程函数
def _enQueueData(dpath, alter, Q):
    flist = glob.glob(dpath) 
    outf = '.' + os.sep + 'tmp' + os.sep + str(os.getpid()) + '.wav'
    thrd = threading.currentThread()
    while getattr(thrd, 'running', True):
        f = flist[randint(0, len(flist) - 1)]
        label = parseName(f)
        if alter:
            soxAlter(f, outf)
            #outf = f
            sps, data = readWav(outf)
            bgnAlter(data)
        else:
            sps, data = readWav(f)
        data = data[1:] - data[0:len(data) - 1] # Z 变换
        Q.put((label, data), True)

# 创建线程，返回线程和队列
def _dataThreadOn(dpath, alter=True, maxQ=128):
    Q = queue.Queue(maxQ)
    thrd = threading.Thread(target=_enQueueData, args = (dpath, alter, Q))
    thrd.start()
    return thrd, Q

# 发送所有数据，阻塞模式
def _sendall(s, data):
    length = len(data)
    minimal = 512
    prog = 0
    prog += s.send(data[0:8])
    while prog < length:
        prog += s.send(data[8:len(data)])
    return None

# 主要函数，创建一个socket，向sock_addr发送数据，并且负责IO线程的管理
def startAlterShipping(port, glob_string, alter=True, maxQ=64):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', port))

    thrd, Q = _dataThreadOn(glob_string, alter=alter, maxQ=maxQ)
    
    try:
        while True :
            label, data = Q.get()
            label = numpy.array([label, data.shape[0]], dtype=numpy.uint32)
            e = _sendall(s, label.tostring() + data.tostring())
            #print('data over')
            Q.task_done()
    except:
        print('Out')
        s.close()
        thrd.running = False
        _, _ = Q.get()
        Q.task_done()
        threading.Thread.join(thrd)

def shippingTrainData():
    startAlterShipping(9009, TRAIN_DATA_DIR + os.sep + '*.wav', maxQ = 50)

def shippingTestData():
    startAlterShipping(9090, TEST_DATA_DIR + os.sep + '*.wav', alter=False, maxQ=500)

def shippingAllMultiProcess(train_num=10):
    p = multiprocessing.Pool()

    for i in range(0, train_num):
        p.apply_async(shippingTrainData, args=())
    
    time.sleep(1)
    shippingTestData()

    p.close()
    p.join()

if __name__ == '__main__':
    shippingAllMultiProcess(train_num=14)
