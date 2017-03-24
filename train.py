#!/opt/anaconda3/bin/python
# -*- coding:utf-8 -*-


from model import KerasModel
from sockDataGenerator import sockDataGenerator

def train(sp=-1):
    model = KerasModel()
    
    train = sockDataGenerator(9009,  50)
    test = sockDataGenerator(9090, 32)
    next(train)
    next(test)
    print('socket esteblish')
    if sp != -1:
        chkp = '.\\models\\save_' + str(sp) + '.h5'
        model.load_weights(chkp)
    print('start point: %d'%sp)

    for i in range(sp + 1, 10):
        model.fit_generator(
            generator=train,
            samples_per_epoch=1000,
            nb_epoch=5,
            validation_data=test,
            nb_val_samples=128
        )
        model.save_weights('.\\models\\save_' + str(i) + '.h5' )

if __name__ == '__main__':
    train(-1)
