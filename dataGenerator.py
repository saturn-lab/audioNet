#!/opt/anaconda3/bin/python

import socket
import os, stat
import numpy as np
import time
import select

import grpc
from augmentation import augGrpc, augPb, SERVER_PORT, CS

MAX_MESSAGE_LENGTH = 90000000

def DataGenerator(data_type = 'train'):
  channel = grpc.insecure_channel(
    'localhost:%d' % SERVER_PORT, 
    options=[('grpc.max_receive_message_length', MAX_MESSAGE_LENGTH)]
  )

  stub = augGrpc.DataProviderStub(channel)
  empty = augPb.Empty()

  ret = stub.Control(CS(sign = CS.START))

  if len(ret.error) != 0:
    raise RuntimeError(ret.error)
  
  if data_type == 'train':
    func = stub.GetTrainData
  elif data_type == 'test':
    func = stub.GetTestData
  else:
    raise ValueError('data_type should be either "train" or "test"')

  while True:
    ret = func(empty)

    data = np.frombuffer(ret.data, dtype = np.float32)
    label = np.frombuffer(ret.label, dtype = np.float32)
    data = data.reshape([ret.batch_size, -1, 1, 1])
    label = label.reshape([ret.batch_size, -1])
    
    yield data, label

if __name__ == '__main__':
    gen = DataGenerator()
    for i in range(0, 100):
        label, d = next(gen)
        print(i, label)
        time.sleep(1)
