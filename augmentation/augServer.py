#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# Classes: Auxiliary, Handler, DataQueue, DataProvider

# Inner Dependences:
#   Auxiliary -> Handler
#   Auxiliary -> DataProvider
#   Handler   -> DataProvider
#   DataQueue -> DataProvider

# Outer Dependences:
#   augmentor.Augmentor -> DataProvider
#   augServer_pb2_grpc  -> DataProvider
#   augServer_pb2       -> Auxiliary

import sys
import grpc
import time
import queue
import zlib
from concurrent.futures import ThreadPoolExecutor

from . import augServer_pb2_grpc as augGrpc
from . import augServer_pb2 as augPb
from .augServer_pb2 import ControlSignal as CS
from . import config

from .augmentor import Augmentor

class Auxiliary:
  @staticmethod
  def getThreadPool(self):
    return ThreadPoolExecutor(
        max_workers = self.train.thread_size + 
        self.test.thread_size)

  @staticmethod
  def getQueueReport(dataq):
    return augPb.QueueReport(
        thread_size = dataq.thread_size,
        queue_capacity = dataq.queue.maxsize,
        queue_size = dataq.queue.qsize(),
        batch_size = dataq.batch_size)

  @staticmethod
  def getStatus(self):
    return augPb.Status(
        running = self.running,
        train = Auxiliary.getQueueReport(self.train),
        test = Auxiliary.getQueueReport(self.test),
        )

  @staticmethod
  def getControlResponse(self, error = None):
    status = Auxiliary.getStatus(self)
    return augPb.ControlResponse(status = status, error = error)
  
  @staticmethod
  def setQueue(queue, setting):
    if setting.batch_size <= 0:
      return False
    queue.batch_size = setting.batch_size
    
    if setting.queue_capacity <= 0:
      return False
    queue.queue.maxsize = setting.queue_capacity

    if setting.thread_size <= 0:
      return False
    queue.thread_size = setting.thread_size

    return True
  
  @staticmethod
  def getBatchData(data, label):
    return augPb.BatchData(
        batch_size = data.shape[0], 
        data = data.tostring(), 
        label = label.tostring())

class Handler:
  HANDLER = None

  @staticmethod
  def startHandler(self, request):
    if self.running:
      return Auxiliary.getControlResponse(self, 'threads are already running')

    self.running = True
    
    for i in range(0, self.train.thread_size):
      self.pool.submit(self.threadEnqueueData, i, 'train')
    for i in range(0, self.test.thread_size):
      self.pool.submit(self.threadEnqueueData, i, 'test')
    
    return Auxiliary.getControlResponse(self)

  @staticmethod
  def stopHandler(self, request):
    if not self.running:
      return Auxiliary.getControlResponse(self, 'threads are already shutdown')

    self.running = False

    self.train.queue.maxsize += self.train.thread_size + 1
    self.test.queue.maxsize += self.test.thread_size + 1
    
    self.pool.shutdown() 
    self.pool = Auxiliary.getThreadPool(self)
    
    return Auxiliary.getControlResponse(self)

  @staticmethod
  def settingHandler(self, request):
    if self.running == True:
      return Auxiliary.getControlResponse(
          self, 
          'Threads are running. Stop them before change anything.')

    status = request.status
    if not Auxiliary.setQueue(status.train):
      return Auxiliary.getControlResponse(self, 'parameters should larger than 0')
    if not Auxiliary.setQueue(status.test):
      return Auxiliary.getControlResponse(self, 'parameters should larger than 0')
    
    return Auxiliary.getControlResponse(self)
  
  @staticmethod
  def getHandler():
    if Handler.HANDLER is not None:
      return Handler.HANDLER

    handler = {}
    handler[CS.SETTING]             = Handler.settingHandler
    handler[CS.START]               = Handler.startHandler
    handler[CS.STOP]                = Handler.stopHandler

    Handler.HANDLER = handler
    
    return handler

class DataQueue:
  def __init__(self, batch_size, thread_size, qsize):
    self.batch_size = batch_size
    self.thread_size = thread_size
    self.queue = queue.Queue(qsize)

class DataProvider(augGrpc.DataProviderServicer):
  def __init__(self):
    self.running = False

    # batch_size, thread_size, qsize
    self.train = DataQueue(
        config.TRAIN_BATCH_SIZE, 
        config.TRAIN_THREAD_SIZE, 
        config.TRAIN_QUEUE_SIZE)
    self.test = DataQueue(
        config.TEST_BATCH_SIZE, 
        config.TEST_THREAD_SIZE, 
        config.TEST_QUEUE_SIZE)

    self.pool = Auxiliary.getThreadPool(self)
    return
  
  @staticmethod
  def getData(queue):
    data = queue.get()
    queue.task_done()

    return data

  # override
  def GetTrainData(self, request, context):
    return DataProvider.getData(self.train.queue)
  
  # override
  def GetTestData(self, request, context):
    return DataProvider.getData(self.test.queue)

  # override
  def GetStatus(self, request, context):
    return Auxiliary.getStatus(self)

  #override
  def Control(self, request, context):
    return Handler.getHandler()[request.sign](self, request)
  
  def threadEnqueueData(self, index, qtype):
    uuid = '%s_%d' % (qtype, index)
    agt = Augmentor(uuid)

    if qtype == 'train':
      func = agt.getTrainBatch
      queue = self.train
    elif qtype == 'test':
      func = agt.getTestBatch
      queue = self.test
    else:
      print(error)
      raise ValueError('qtype must be one of "train", "cv" and "test"')
    
    new_gen = True
    while self.running:
      if new_gen:
        data, label = func(queue.batch_size)
        bd = Auxiliary.getBatchData(data, label)
      
      try:
        queue.queue.put_nowait(bd)
        new_gen = True
      except:
        time.sleep(0.03)
        new_gen = False

    return
 
  def run(self):
    server = grpc.server(ThreadPoolExecutor(max_workers = 5))
    augGrpc.add_DataProviderServicer_to_server(self, server)
    server.add_insecure_port('[::]:%d' % config.SERVER_PORT)
    server.start()
    try:
      while True:
        time.sleep(99999)
    except KeyboardInterrupt:
      self.running = False
      self.pool.shutdown()
      server.stop(0)

if __name__ == '__main__':
  a = DataProvider()
  a.run()
