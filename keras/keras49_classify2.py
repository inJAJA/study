# 다중 분류 

""" 과제  1. y이의 dim을 6에서 5로 변경하시오
          2. y_pred를 숫자로 바꿔라!
"""
import numpy as np
from keras.models import Sequential
from keras.layers import Dense

from keras.utils import np_utils
# from keras.utils import to_categorical

#1. 데이터
x = np.array(range(1, 11))
y = np.array([1, 2, 3, 4, 5, 1, 2, 3, 4, 5])


"""One_Hot_Encoding"""
y = np_utils.to_categorical(y)                  
# y = to_categorical(y)
""" 
- 다중분류 모델은 반드시 one_hot_encoding사용
- 다중 클래스 분류 문제가 각 클래스 간의 관계가 균등해야 하기 떄문에
  ex) 원핫인코딩 사용안할 시  : y가 1 과 5로 분류된다면 5에 값이 치중된다.

- 해당 숫자에 해당되는 자리만 1이고 나머지는 0으로 채운다. 
- '0'부터 인덱스가 시작이다.                                                              
  \ 자리 : 0   1   2   3   4   5     => 분류되는 수만큼 증폭된다. (10, )                               
  숫자 ---------------------------                              (10, 5)
       1 : 0   1   0   0   0   0                                    
       2 : 0   0   1   0   0   0
       3 : 0   0   0   1   0   0
       4 : 0   0   0   0   1   0
       5 : 0   0   0   0   0   1  
"""

print(y)                    
print(y.shape)                     # (10, 6)  : 자동으로 0을 인식해서 6개(dimension이 늘어남)

y = y[:, 1:]                       # 우리는 column이 5개(원래 dimension)임으로 reshape해준다.
print(y.shape)                     # (10, 5) 


#2. 모델 구성
model = Sequential()
model.add(Dense(200,activation = 'relu', input_dim = 1))
model.add(Dense(150,activation = 'relu'))
model.add(Dense(120,activation = 'relu'))
model.add(Dense(90,activation = 'relu'))
model.add(Dense(60,activation = 'relu'))
model.add(Dense(40,activation = 'relu'))
model.add(Dense(30,activation = 'relu'))
model.add(Dense(20,activation = 'relu'))
model.add(Dense(10,activation = 'relu'))        
model.add(Dense(5,activation = 'softmax'))
""" 다중 분류는 'softmax' 사용
  : output들의 합이 1이 되도록 출력하는 함수
"""




#3. 컴파일, 훈련
model.compile(loss = 'categorical_crossentropy', optimizer = 'adam', metrics = ['acc'])    # acc : 분류 모델 0 or 1
model.fit(x, y, epochs = 90, batch_size =1)
""" loss = 'categorical_crossentropy' : 다중분류에서 사용 """



#4. 평가, 예측
loss, acc = model.evaluate(x, y, batch_size= 1)
print('loss :', loss)
print('acc :', acc)


x_pred = np.array([1, 2, 3])
y_pred = model.predict(x_pred)                    
print('y_pred :', y_pred)
print(y_pred.shape)                               # (3, 5)
""" x 하나 집어 넣으면 [ 5 ]개가 나옴 (one_hot_encoding때문)
y_pred : [[0.20067349 0.19978711 0.19959101 0.2001942  0.19975421]
         [0.20067349 0.19978711 0.19959101 0.2001942  0.19975421]
         [0.20067349 0.19978711 0.19959101 0.2001942  0.19975421]]

# 이상적인 값
   [ 1   2   3   4   5 ]
y1 : 1   0   0   0   0    => 1
y2 : 0   1   0   0   0    => 2
y3 : 0   0   1   0   0    => 3
"""



"""
one_hot_decoder
: np.argmax()
: 최대값의 색인 위치를 찾는다.

"""
#1. 함수 사용
def decode(datum):
    return np.argmax(datum)
  
for i in range(y_pred.shape[0]):                   # y_pred.shape[0] = 3, i = [0, 1, 2]                     
    y2_pred = decode( y_pred[i])       
    print('y2_pred:', y2_pred + 1)

#2. axis 사용               # 열 하나하나로 비교하겠다.
y3_pred = np.argmax(y_pred, axis= 1) + 1           # 뒤로 한자리씩 넘겨준다.
print(y3_pred)                                     # y3_pred = [1, 2, 3]

"""
x = [[1, 1],
     [2, 2]] 이고 sum을 실행 한다고 하면

# aixs = 0             # axis = 1 
: 행에 대한 연산         : 열에 대한 연산      sum
     [[ 1, 1 ],               [[ 1, 1 ],  = [ 2    
      [ 2, 2 ]]                [ 2, 2 ]]  =   4 ]
      --------
sum = [ 3  4 ]                     
"""