#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# a client sample

import augServer_pb2 as augPb
import augServer_pb2_grpc as augGrpc
import grpc
import time
import numpy as np
import zlib

from augServer_pb2 import ControlSignal as CS

import config
MAX_MESSAGE_LENGTH = 90000000

channel = grpc.insecure_channel(
    'localhost:%d' % config.SERVER_PORT, 
    options=[('grpc.max_receive_message_length', MAX_MESSAGE_LENGTH)]
    )

stub = augGrpc.DataProviderStub(channel)

empty = augPb.Empty()
#print(stub.GetStatus(empty))

#print(stub.Control(CS(sign = CS.START)))
#print(stub.Control(CS(sign = CS.STOP)))
#time.sleep(0.5)
#exit()

t1 = time.time()
bd = stub.GetTrainData(empty)
batch_size = bd.batch_size

data = np.frombuffer(bd.data, dtype = np.float32)
label = np.frombuffer(bd.label, dtype = np.int32)
lens = np.frombuffer(bd.lens, dtype = np.int32)
print(data.shape)
print(label.shape)
print(lens.shape)
t2 = time.time()
print(t2 - t1)
