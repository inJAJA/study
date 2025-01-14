import os
import cv2
import glob
from tensorflow.keras.models import load_model
import efficientnet.tfkeras as efn
from tensorflow.keras.models import load_model, Model

# import sklearn as sk
import h5py
import numpy as np

image_path = 'D:/data/HUMAN_face.hdf5'
f = h5py.File(image_path, 'r')

model = load_model('D:/weight/efficientnet_true2.hdf5')

filename = os.listdir('D:\FFHQ')    # 원본 이미지 불러오기 위한 파일 이름

# import keras.backend.tensorflow_backend as K
t = open("./GAN/predict_list.txt", 'w', encoding='utf-8')

for s in range(0, 70400, 100):
    batch = s + 100

    x = f['autoencoder'][s:batch]
    fl = filename[s:batch]

    for x_pred, ff in zip(x, fl):
        x_pred = x_pred[None, ...]
        # x_pred = x_pred.reshape(1, 256, 256, 3)

        prediction = model.predict(x_pred)

        per = np.round(np.max(prediction, axis = 1)*100, 2)

        one = np.argmax(prediction, axis = 1) + 1
        print(ff, '예측값 :', one, 'max :', per)

        img = cv2.imread('D:/FFHQ/'+ff, cv2.IMREAD_COLOR)
        cv2.imwrite('D:/predict/%i/%s_%d.jpg'%(one, ff, per), img)
        t.write(ff+' '+str(one[0])+' '+str(per[0]) + '\n' )


'''
# 카테고리 불러오기
categories = ['Bichon_frise', 'Border_collie', 'Bulldog', 'Chihuahua',
              'Corgi', 'Dachshund', 'Golden_retriever', 'huskey',
              'Jindo_dog', 'Maltese', 'Pug', 'Yorkshire_terrier',
              'Doberman', 'Italian_greyhound','Pekingese', 'Sichu']

img_path = 'D:/data/breed_test/test_set'
filename = os.listdir(img_path)

#우리가 테스트 폴더 안에 있는 이미지의 이름들이 각각의 매칭되는 견종 이름으로 되어 있다 그 견종이 뭔지 확인을 하기위해서 이렇게 써 주었다. 
#파일 이름이 견종 이름이여야지만 사용할 수 있는 , 그 파일이 뭐로 예측되어 있는지 알려고 할때 사용할수 있다. 
for i in range(len(number)):
    idex = number[i]
    true = filename[i].replace('.jpg', '').replace('.png','')
    pred = categories[idex]
    print('실제 :', true, '\t예측 견종 :', pred)
'''

