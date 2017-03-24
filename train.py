#!/opt/anaconda3/bin/python

from model import KerasModel
from sockDataGenerator import sockDataGenerator

def train(sp=-1):
    model = KerasModel()
    
    train = sockDataGenerator(9009,  2)
    test = sockDataGenerator(9090, 2)
    next(train)
    next(test)
    print('socket esteblish')
    if sp != -1:
        chkp = '.' + os.sep + 'models' + os.sep + 'save_' + str(sp) + '.h5'
        model.load_weights(chkp)
    print('start point: %d'%sp)

    for i in range(sp + 1, 100):
        model.fit_generator(
            generator=train,
            steps_per_epoch=500,
            epochs=5,
            validation_data=test,
            validation_steps=10,
        )
        model.save_weights('.' + os.sep + 'models' + os.sep + 'save_' + str(i) + '.h5' )

if __name__ == '__main__':
    train(-1)
