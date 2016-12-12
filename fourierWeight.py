#!/usr/bin/env python
import numpy
def fourierWeight(length, fraction=16.0):
    freq_length = length/fraction
    sample_index= numpy.array([range(0, length)], dtype=numpy.float32)
    freq_index = numpy.array([range(0, length)], dtype=numpy.float32)
    freq_index = freq_index/fraction

    w = numpy.matmul(numpy.transpose(sample_index), freq_index)
    w = w*(2*numpy.pi)/length # phi = 2*PI*i*k/n
    sines = -numpy.sin(w)/length # e(-j*phi) = -jsin(phi) + cos(phi)
    cosines = numpy.cos(w)/length

    # para-curve window  f(0) = 0; f(n-1) = 0;  f((n-1)/2) = 1
    window = numpy.array(xrange(0, length), dtype=numpy.float32)
    window = numpy.reshape(window, [length, 1])
    window = (window * 4.0 / (length - 1)) - numpy.multiply(window, window) * 4.0 / ((length - 1) * (length - 1))
    
    sines = numpy.multiply(window, sines)
    cosines = numpy.multiply(window, cosines)
    sines = numpy.reshape(sines, [length, 1, 1, -1])
    cosines = numpy.reshape(cosines, [length, 1, 1, -1])
    return sines, cosines

if __name__ == '__main__':
    fourierWeight(101)
