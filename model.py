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
    Convolution2D, 
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
    
    x = Convolution2D(filters=32, kernel_size=(3, 3), strides=(3,3), activation='relu', kernel_regularizer=l2(L2_RATE))(x)
    
    #x = Convolution2D(filters=64, kernel_size=(3, 3), strides=(3,3), activation='relu', kernel_regularizer=l2(L2_RATE))(x)
    
    #x = Convolution2D(filters=64, kernel_size=(3, 3), strides=(2,2), activation='relu', kernel_regularizer=l2(L2_RATE))(x)
    
    #x = Convolution2D(filters=32, kernel_size=(3, 3), strides=(2,2), activation='relu', kernel_regularizer=l2(L2_RATE))(x)
    
    #x = Convolution2D(filters=16, kernel_size=(3, 3), strides=(2,2), activation='relu', kernel_regularizer=l2(L2_RATE))(x)
    
    freq, chan = x.get_shape()[2:4]
    x = TimeDistributed(Reshape([int(freq)*int(chan)]))(x)
    print(x.get_shape())
    x = Bidirectional(LSTM(64, ))(x)
    
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
