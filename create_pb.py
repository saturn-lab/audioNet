from model import KerasModel
from tensorflow.python.framework import graph_io
from tensorflow.python.training import saver
from keras import backend as K
import os

model = KerasModel()
sp = 64
chkp = '.' + os.sep + 'models' + os.sep + 'save_' + str(sp) + '.h5'

sess = K.get_session()
model.load_weights(chkp)
ckpt_path = saver.Saver().save(sess, "models/model.ckpt")
graph_io.write_graph(sess.graph, './models', 'model.pb')

command = '''python -m tensorflow.python.tools.freeze_graph \
--input_graph=%s \
--input_checkpoint=%s \
--output_graph=%s \
--output_node_names=%s \
''' % (
    os.join('.', 'models', 'model.pb'),
    os.join('.', 'models', 'model.ckpt'),
    os.join('.', 'model.pb'),
    '"dense_2/Softmax"'
)

os.system(command)