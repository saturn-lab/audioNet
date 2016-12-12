#!/usr/bin/env python

import tensorflow as tf
import numpy
from sockDataGenerator import sockDataGenerator
from fourierWeight import fourierWeight

def model():
    datain = tf.placeholder(tf.float32, [None, None, 1, 1])
    sinW, cosW = fourierWeight(1000, 4)
    
    sin = tf.nn.conv2d(datain, sinW, [1,100,1,1], padding='VALID')
    cos = tf.nn.conv2d(datain, cosW, [1,100,1,1], padding='VALID')
    
    spc = tf.complex(cos, sin)
    dataout = tf.complex_abs(spc)

    dg = sockDataGenerator()
    with tf.Session() as sess:
        tf.initialize_all_variables().run()
        for i in xrange(0, 1):
            label, data = dg.next()
            do = sess.run(dataout, feed_dict={datain: data})
            numpy.save('./out.npy', do)

if __name__ == '__main__':
    model()
