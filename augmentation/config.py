#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import os

ME_DIR = os.path.dirname(os.path.realpath(__file__))
DATA_DIR = os.path.join(ME_DIR, '..', 'data')

SERVER_PORT = 50051

TRAIN_BATCH_SIZE = 16
TRAIN_THREAD_SIZE = 4
TRAIN_QUEUE_SIZE = 10

TEST_BATCH_SIZE = 50
TEST_THREAD_SIZE = 1
TEST_QUEUE_SIZE = 50
