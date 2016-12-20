#!/usr/bin/env python

import socket
import os
import numpy
import time
import select

def _recvall(r, length):
    minimal = 4096
    if length > minimal:
        data = r.recv(minimal)
        length = length - len(data)
    else:
        data = r.recv(length)
        length = length - len(data)
    
    while length > minimal:
        B = r.recv(minimal)
        data += B
        length = length - len(B)

    while length > 0:
        B =  r.recv(length)
        data += B
        length = length - len(B)

    return data

def sockDataGenerator(path='./train.sock'):
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    os.system('rm -rf ' + path)
    s.bind(path)
    s.listen(5)
    
    inputs = [s]

    while True:
        rs, _, _ = select.select(inputs, [], [], 1)
        for r in rs:
            if r is s:
                clientSock, clientAddr = r.accept()
                inputs.append(clientSock)
            else:
                dataL = r.recv(8)
                if len(dataL) != 8:
                    r.close()
                    inputs.remove(r)
                else:
                    dL = numpy.fromstring(dataL, dtype=numpy.uint32)
                    if dL[1] == 0:
                        r.close()
                        inputs.remove(r)
                    else:
                        data = _recvall(r, dL[1] * 4)
                        d = numpy.fromstring(data, dtype=numpy.float32)
                        d = d.reshape([1, -1, 1, 1])
                        L = numpy.zeros([1, 24], dtype=numpy.float32)
                        L[0][dL[0]] = 1.0
                        yield d, L



if __name__ == '__main__':
    gen = sockDataGenerator()
    for i in xrange(0, 100):
        label, d = gen.next()
        print i, label
        time.sleep(1)
