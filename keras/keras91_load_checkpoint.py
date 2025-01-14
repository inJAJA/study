import numpy as np
import matplotlib.pyplot as plt

from keras.datasets import mnist                         
mnist.load_data()                                         

(x_train, y_train), (x_test, y_test) = mnist.load_data() 
print(x_train[0])                                         
print('y_train: ' , y_train[0])                           # 5

print(x_train.shape)                                      # (60000, 28, 28)
print(x_test.shape)                                       # (10000, 28, 28)
print(y_train.shape)                                      # (60000,)       
print(y_test.shape)                                       # (10000,)



# 데이터 전처리 1. 원핫인코딩 : 당연하다             
from keras.utils import np_utils
y_train = np_utils.to_categorical(y_train)
y_test = np_utils.to_categorical(y_test)
print(y_train.shape)                                      #  (60000, 10)

# 데이터 전처리 2. 정규화( MinMaxScalar )                                                    
x_train = x_train.reshape(60000, 28, 28, 1).astype('float32') /255  
x_test = x_test.reshape(10000, 28, 28, 1).astype('float32') /255.                                     

'''
#2. 모델 구성
from keras.models import Sequential
from keras.layers import Dense, Conv2D, Flatten, MaxPooling2D
model = Sequential()
model.add(Conv2D(100, (2, 2), input_shape  = (28, 28, 1), padding = 'same'))
model.add(MaxPooling2D(pool_size=2))
model.add(Conv2D(80, (2, 2), padding = 'same'))
model.add(MaxPooling2D(pool_size=2))
model.add(Conv2D(60, (2, 2), padding = 'same'))
model.add(MaxPooling2D(pool_size=2))
model.add(Conv2D(40, (2, 2),padding = 'same'))
model.add(Conv2D(20, (2, 2),padding = 'same'))
model.add(Conv2D(10, (2, 2), padding='same'))
model.add(Flatten())
model.add(Dense(10, activation='softmax'))                

model.summary()



# EarlyStopping
from keras.callbacks import EarlyStopping, ModelCheckpoint
es = EarlyStopping(monitor = 'loss', patience = 20, mode= 'auto')
# Modelsheckpoint
modelpath = './model/check-{epoch:02d}-{val_loss:.4f}.hdf5'
checkpoint = ModelCheckpoint(filepath = modelpath, monitor = 'val_loss', 
                            verbose =1,
                            save_best_only= True, save_weights_only= False)
                                                 # 가중치만 저장하겠다 : False

#3. 훈련                      
model.compile(loss = 'categorical_crossentropy', optimizer = 'adam', metrics= ['acc']) # metrics=['accuracy']
hist = model.fit(x_train, y_train, epochs= 10, batch_size= 64, callbacks = [es, checkpoint],
                                   validation_split=0.2, verbose = 1)

'''
from keras.models import load_model                     # (save_wights_only = False)
model = load_model('./model/check-08-0.0540.hdf5')      # model과 weight가 같이 저장되어 있음 
                                                        # model, compile, fit부분이 필요없다.
                                                        

#4. 평가
loss_acc = model.evaluate(x_test, y_test, batch_size= 64)
print('loss_acc: ', loss_acc)                     

                         

'''     
loss_acc:  [0.041936698463978246, 0.9876999855041504]
'''


"""
# model, weight 저장 방법들:

1. model.save( '경로/ 파일명' )
  1) fit 전 
    : model을 저장한다.                 -> compile, fit 필요 O, layer추가 가능
  2) fit 후 
    : model과 최종 weight을 저장한다.    -> compile, fit 필요 X

    # from keras.models import load_model
      model = load_model('./model/model_test01.h5')


2. model.save_weights( '경로/ 파일명' ) 
   : 각 레이어의 weight를 저장한다.      -> model, compile 필요 O
                                          : weight를 저장한 model과 구성이 같아야 한다.
                                            -> 저장된 각 레이어의 weight가 model과 매치되어야 하기 때문에  
    
    # model.load_weights('./model/test_weight1.h5')


3. Modelcheckpoint
   1) save_weights_only = True
    : 각 epoch마다의 weight를 저장한다  
   2)      ,,           = False
    : model과 각 epoch마다의 weight를 저장한다. 
                                        -> model, compile, fit 필요 X
    
    # from keras.models import load_model                     # (save_wights_only = False)
      model = load_model('./model/check-08-0.0540.hdf5') 



### model.save & model.save_weight 과 ModelCheckpoint 중 뭐가 더 좋은 지는 정확하지 않다.
### => 결과 값( loss, acc)을 보고 더 좋은 것을 사용한다. 

"""