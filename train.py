#!/opt/anaconda3/bin/python
from model import KerasModel
from dataGenerator import DataGenerator
import os

from keras.models import load_model
 #确定时代的次数，对应的为权重保存的次数
epochs_time=1

def train(sp=-1):
    model = KerasModel()
    train = DataGenerator('train')
    test = DataGenerator('test')
    
    if sp != -1:
        chkp = '.' + os.sep + 'models' + os.sep + 'save_' + str(sp) + '.h5'
        model.load_weights(chkp)
        print('start point: %d'%sp)
    print("开始训练：")
  
    model.fit_generator(    
        generator=train,
        #steps_per_epoch：在声明一个epoch完成并开始下一个epoch之前从generator产生的总步数，它通常应该等于你的数据集的样本数量除以批量大小，对于Sequence，它是可选的，如果未指定，将使用len（generator）作为步数
        #按理说是按照上面的标准进行的，但是因为我们数据集较少，所以我们使用更多的数量跑
        #在测试的时候我运用的是14是完全按照理论做的
        #如果现在的次数不能够正常运行请重新改回14并增加时代
        steps_per_epoch=3000，
        #epochs 确定世代的次数
        epochs=epochs_time,
        verbose=1,
        #validation_steps是步长
        validation_steps=100
        #想要了解更多fit_generator的参数：https://blog.csdn.net/qq_32951799/article/details/82918098
    )
        #每个世代的模型都做保存
    model.save_weights('.' + os.sep + 'models' + os.sep + 'save_' +str(epochs_time)+ '.h5' )



if __name__ == '__main__':
    train(-1)
