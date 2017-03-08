#!/opt/anaconda3/bin/python

import socket
import os, stat
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

def sockDataGeneratorOrigin(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    s.bind(('', port))
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
                        d = d.reshape([-1])
                        L = numpy.zeros([24], dtype=numpy.float32)
                        L[dL[0]] = 1.0
                        yield d, L, r

def sockDataGenerator(port, batchSize = 16):
    dg = sockDataGeneratorOrigin(port)
    while True:
        dlist = []
        ret_L = numpy.zeros([batchSize, 24], dtype = numpy.float32)
        for i in range(0, batchSize):
            d, L, _ = next(dg)
            dlist.append(d)
            ret_L[i, :] = L

        lengthes = [d.shape[0] for d in dlist]
        ret_d = numpy.zeros([batchSize, max(lengthes)], dtype=numpy.float32)

        for i, d in enumerate(dlist):
            ret_d[i, 0:lengthes[i]] = d
        
        ret_d = ret_d.reshape(batchSize, -1, 1, 1)
        yield ret_d, ret_L


if __name__ == '__main__':
    gen = sockDataGenerator()
    for i in range(0, 100):
        label, d = next(gen)
        print(i, label)
        time.sleep(1)
