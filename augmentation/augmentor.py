#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# Classes: Augmentor

# Outer Dependencies:
#   soxAlter.soxAlter  ->  Augmentor
#   dataset.DataSet    ->  Augmentor

import os
import wave
import random
import numpy as np


from .soxAlter import soxAlter
from .dataset import Dataset
from .backgroundAlter import bgnAlter

TMP_DIR = os.path.dirname(os.path.realpath(__file__))
TMP_DIR = os.path.join(TMP_DIR, 'tmp')

def pack(wavs):
  data_len = [i.shape[0] for i in wavs]
  dl_max = max(data_len)
  
  data = np.zeros(shape=[len(wavs), dl_max], dtype = np.float32)
  for i, wav_i in enumerate(wavs):
    data[i, - wav_i.shape[0]:] = wav_i
    
  data = data/32768.0

  return data

class Augmentor:
  def __init__(self, index):
    self.index = index

  def augWave(self, fin, is_train):
    fout = os.path.join(TMP_DIR, '%s.wav' % self.index)
    
    if is_train:
      soxAlter(fin, fout)
    else:
      fout = fin
      
    with wave.open(fout, 'rb') as f:
      data = f.readframes(f.getnframes())
    data = np.frombuffer(data, np.int16)
    data = data / 32768.0

    if is_train:
      data = bgnAlter(data)
    
    return data
  
  def getBatch(self, size, data_list, is_train = True):
    batch = random.sample(data_list, size)
    wavs = [self.augWave(f, is_train) for f in batch]

    return pack(wavs), Dataset.NamesToLabel(batch)

  def getTrainBatch(self, size):
    return self.getBatch(size, Dataset.TRAIN_LIST)

  def getTestBatch(self, size):
    return self.getBatch(size, Dataset.TEST_LIST, is_train = False)

if __name__ == '__main__':
  a = Augmentor(1)
  data, label = a.getTrainBatch(2)
  
