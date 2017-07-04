
from model import KerasModel
from tensorflow.python.framework import graph_io
from tensorflow.python.training import saver
from keras import backend as K

model = KerasModel()
sp = 64
chkp = '.' + os.sep + 'models' + os.sep + 'save_' + str(sp) + '.h5'
model.load_weights(chkp)

sess = K.get_session()
ckpt_path = saver.Saver().save(sess, "models/model.ckpt")
graph_io.write_graph(sess.graph, './models', 'model.pb')


```
Run Python: 
python -m tensorflow.python.tools.freeze_graph 
--input_graph=./models/model.pb 
--input_checkpoint=./models/model.ckpt
--output_graph=./model.pb 
--output_node_names="dense_2/Softmax"
```