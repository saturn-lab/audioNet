#/usr/bin/env python3
# -*- coding:utf-8 -*-

import os
import sys
import glob
import numpy as np

from . import config

class Auxiliary:
  ME_DIR = os.path.dirname(os.path.realpath(__file__))
  
  @staticmethod
  def GetWavList(wav_dir):
    if not os.path.isdir(wav_dir):
      raise ValueError('"%s" is not a existing folder.' % data_dir)
    wavs = glob.glob(os.path.join(wav_dir, '*.wav'))

    return wavs

class Dataset:
  DATA_DIR = config.DATA_DIR
  TRAIN_DIR = os.path.join(DATA_DIR, 'train')
  TEST_DIR = os.path.join(DATA_DIR, 'test')
  
  TRAIN_LIST = Auxiliary.GetWavList(TRAIN_DIR)
  TEST_LIST = Auxiliary.GetWavList(TEST_DIR)
  LABELS = np.eye(24, dtype=np.float32)
  
  @staticmethod
  def NamesToLabel(file_names):
    ids = [int(f.split('_')[-1].split('.')[0]) for f in file_names]
    data = Dataset.LABELS[ids]

    return data
