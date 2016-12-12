#!/usr/bin/env python
import numpy
from PIL import Image
data = numpy.load('./out.npy')
data = data.reshape([-1, data.shape[3]])
data = data - data.min()
data = data/data.max()

A = 5

data = data * A
data = data + 1

data = numpy.log(data)

data = data/data.max()

data = data * 255.0

img = Image.fromarray(data)
img = img.convert('RGB')
img.save('/home/saturn/ds/publicStorage/test.jpg')
