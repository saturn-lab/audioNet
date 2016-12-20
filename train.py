#!/usr/bin/env python
# -*- coding:utf-8 -*-

from model import KerasModel
from sockDataGenerator import sockDataGenerator

def train(sp=-1):
    model = KerasModel()
    
    train = sockDataGenerator('train.sock')
    test = sockDataGenerator('test.sock')
    train.next()
    test.next()
    
    if sp != -1:
        chkp = './models/save_' + str(sp) + '.h5'
        model.load_weights(chkp)
    for i in xrange(sp + 1, 100):
        model.fit_generator(
            generator=train,
            samples_per_epoch=1700,
            nb_epoch=20,
            validation_data=test,
            nb_val_samples=64
        )
        model.save('./models/save_' + str(i) + '.h5' )

if __name__ == '__main__':
    train(14)
