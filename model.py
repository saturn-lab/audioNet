#!/opt/anaconda3/bin/python

import tensorflow as tf
import numpy
from sockDataGenerator import sockDataGenerator
from fourierWeight import fourierLayer, fourierLayerShape, fourierWeight

from keras.models import Model
from keras.regularizers import l2
from keras.optimizers import Adam
from keras.layers import (
    Input, 
    Dense, 
#    Convolution2D, 
    Conv2D, 
    Lambda, 
    Activation, 
    Flatten,
    Dropout,
    Bidirectional,
    LSTM,
    Reshape,
    TimeDistributed
)

DROP_RATE=0.5
L2_RATE=0.0001

def KerasModel(isCompile=True):
    In = Input(shape=(None, 1, 1))
    x = Lambda(fourierLayer, output_shape=fourierLayerShape)(In)
    #x = Convolution2D(32, 7, 7, subsample=(3,3), activation='relu', W_regularizer=l2(L2_RATE))(x)
    x = Conv2D(32, (7, 7), activation='relu', subsample=(3,3), W_regularizer=l2(L2_RATE))(x)
    #x = Dropout(DROP_RATE)(x)
    #x = Convolution2D(64, 7, 5, subsample=(3,3), activation='relu', W_regularizer=l2(L2_RATE))(x)
    x = Conv2D(64, (7, 5), activation='relu', subsample=(3,3),  W_regularizer=l2(L2_RATE))(x)    
    #x = Dropout(DROP_RATE)(x)
    #x = Convolution2D(64, 3, 3, subsample=(2,2), activation='relu', W_regularizer=l2(L2_RATE))(x)
    x = Conv2D(64, (3, 3), activation='relu', subsample=(2,2), W_regularizer=l2(L2_RATE))(x)    
    #x = Dropout(DROP_RATE)(x)
    #x = Convolution2D(32, 3, 3, subsample=(2,2), activation='relu', W_regularizer=l2(L2_RATE))(x)
    x = Conv2D(32, (3, 3), activation='relu', subsample=(2,2), W_regularizer=l2(L2_RATE))(x)    
    #x = Dropout(DROP_RATE)(x)
    
    freq, chan = x.get_shape()[2:4]
    x = TimeDistributed(Reshape([int(freq)*int(chan)]))(x)
    
    x = Bidirectional(LSTM(128, ))(x)
    
    #x = Dropout(DROP_RATE)(x)
    x = Dense(64, activation='relu')(x)
    #x = Dropout(DROP_RATE)(x)
    x = Dense(24, activation='softmax')(x)
    
    model = Model(inputs=In, outputs=x)
    
    if isCompile:
        opt = Adam(1e-4)
        model.compile(
            optimizer=opt,
            loss='categorical_crossentropy',
            metrics=['accuracy'],
        )

    return model

if __name__ == '__main__':
    #model()
    KerasModel()
