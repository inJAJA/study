import numpy as np
datasets = np.load('./data/iris_save.npy')
print(datasets.shape)                          # (150, 5)

x = datasets[:, :4]                            # (150, 4)
y = datasets[:, 4:]                            # (150, 1)

# x : scaler
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
scaler.fit(x)
x = scaler.transform(x)

# y : one hot encoding
from keras.utils.np_utils import to_categorical
y = to_categorical(y)
print(y.shape)                                 # (150, 3)

from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, y, train_size =0.8,random_state= 10)


#2. model
from keras.models import Sequential
from keras.layers import Dense, Dropout
model = Sequential()
model.add(Dense(10, input_shape = (4, ), activation = 'relu'))
model.add(Dense(50, activation = 'relu'))
model.add(Dropout(0.1))
model.add(Dense(50, activation = 'relu'))
model.add(Dropout(0.1))
model.add(Dense(50, activation = 'relu'))
model.add(Dropout(0.1))
model.add(Dense(50, activation = 'relu'))
model.add(Dropout(0.1))
model.add(Dense(50, activation = 'relu'))
model.add(Dropout(0.1))
model.add(Dense(50, activation = 'relu'))
model.add(Dropout(0.1))
model.add(Dense(50, activation = 'relu'))
model.add(Dropout(0.1))
model.add(Dense(50, activation = 'relu'))
model.add(Dropout(0.1))
model.add(Dense(3, activation = 'softmax'))



# callbacks 
from keras.callbacks import EarlyStopping, TensorBoard, ModelCheckpoint
# earlystopping
es = EarlyStopping(monitor = 'val_loss', patience = 50, verbose =1)
# Tensorboard
ts_board = TensorBoard(log_dir = 'graph', histogram_freq= 0,
                      write_graph = True, write_images=True)
# Checkpoint
modelpath = './model/sample/iris/iris_checkpoinit_best_{epoch:02d}-{val_loss:.4f}.hdf5'
checkpoint = ModelCheckpoint(filepath = modelpath, monitor = 'val_loss',
                            save_best_only= True, save_weights_only = False)


#3. compile, fit
model.compile(loss = 'categorical_crossentropy', optimizer = 'adam', metrics = ['acc'])
hist = model.fit(x_train, y_train, epochs =100, batch_size= 64,
                validation_split = 0.2, verbose = 2,
                callbacks = [es #, checkpoint
                ])


# evaluate
loss, acc = model.evaluate(x_test, y_test, batch_size = 64)
print('loss: ', loss )
print('acc: ', acc)

# graph
import matplotlib.pyplot as plt
plt.figure(figsize = (10, 5))

# 1
plt.subplot(2, 1, 1)
plt.plot(hist.history['loss'], c= 'red', marker = '^', label = 'loss')
plt.plot(hist.history['val_loss'], c= 'cyan', marker = '^', label = 'val_loss')
plt.title('loss')
plt.xlabel('epochs')
plt.ylabel('loss')
plt.legend()

# 2
plt.subplot(2, 1, 2)
plt.plot(hist.history['acc'], c= 'red', marker = '^', label = 'acc')
plt.plot(hist.history['val_acc'], c= 'cyan', marker = '^', label = 'val_acc')
plt.title('accuarcy')
plt.xlabel('epochs')
plt.ylabel('acc')
plt.legend()

"""
loss:  0.01989690773189068
acc:  1.0
"""
