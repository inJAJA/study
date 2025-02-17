import numpy as np
import cv2
import re
import os
from tensorflow.keras.models import load_model
from class_project import Project
import matplotlib.pyplot as plt


# data
#------------- only one file -------------------
image = 'D:/data/project/face_test/face.jpg'
dog = './project/project02/weight/dogHeadDetector.dat'
human = './project/project02/weight/mmod_human_face_detector.dat'

def face_image(image, det_path, w, h):
    img = cv2.imread(image)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    p = Project()
    dets = p.face_detector(img, det_path)

    X = []
    x = X.append
    for i, d in enumerate(dets):
        bbox = p.BBox(i, d)
            
        img_crop = p.crop()
        img_result = cv2.resize(img_crop, dsize = (w, h), interpolation= cv2.INTER_LINEAR)
        x(img_result/255)

    x_pred = np.array(X).reshape(-1, w, h, 3)                
    return x_pred

# f = os.listdir('D:/data\project/breed_final')
# print(f)

x_pred = face_image(image, human, 128, 128 )
print(x_pred.shape)


# load_model
model = load_model('./project/project02/model_save/best_xception.hdf5')

#------------------------------- XAI -------------------------------
from lime.lime_image import LimeImageExplainer
top_labels = 3

try: 
    explainer = LimeImageExplainer()
    explanation = explainer.explain_instance(x_pred[0], model.predict,hide_color = 0, top_labels = top_labels, num_samples = 1000)

    from skimage.segmentation import mark_boundaries
    ind = explanation.top_labels[0]
    dict_heatmap = dict(explanation.local_exp[ind])
    heatmap = np.vectorize(dict_heatmap.get)(explanation.segments)

    plt.imshow(heatmap, cmap = 'RdBu', vmin = -heatmap.max(), vmax = heatmap.max())
    plt.colorbar()
    #--------------------------------------------------------------

    # predict
    prediction = model.predict(x_pred)
    number = np.argmax(prediction, axis = 1)

    # 카테고리 불러오기
    categories = ['Bichon_frise', 'Border_collie', 'Bulldog', 'Chihuahua', 'Corgi', 'Dachshund', 
                        'Golden_retriever', 'Husky', 'Jindo_dog', 'Maltese', 'Pug', 'Yorkshire_terrier']

    '''
    # filename = os.listdir(path)
    filename = ['bichon']

    for i in range(len(number)):
        idex = number[i]
        true = filename[i].replace('.jpg', '').replace('.png','')
        pred = categories[idex]
        print('실제 :', true, '\t예측 견종 :', pred)
    '''
    for i in range(len(number)):
        idex = number[i]
        pred = categories[idex]
        print('예측 견종 :',pred  )
    plt.show()

except:
    print('인식된 사진이 없습니다.')
