""" Data """
import pandas as pd
import numpy as np

# DataFrame을 만들때 index, columns을 설정하지 않으면 
# 기본값으로 0부터 시작하는 정수형 숫자로 입력된다.
a = pd.DataFrame(np.random.randn(6, 4))     # a.shape = (6, 4)
print(a)
#           0         1         2         3
# 0  0.808303  1.552849  0.042347 -0.184805
# 1 -1.753576  0.145659 -0.607672  0.192335
# 2  2.302297 -0.292741 -0.488121  0.626413
# 3  0.874976 -0.595036 -0.592076 -1.322285
# 4  1.776044 -1.156277  0.720918 -0.485035
# 5 -1.814656  0.458943  0.084311  1.280962


# 열의 key설정
a.columns = ['A','B','C','D']
print(a.columns)
# Index(['A', 'B', 'C', 'D'], dtype='object')


# 연속된 날짜, 시각 등을 생성
a.index = pd.date_range('20160701', periods =6)
print(a.index)
# DatetimeIndex(['2016-07-01', '2016-07-02', '2016-07-03', 
#                '2016-07-04','2016-07-05', '2016-07-06'],
#                        dtype='datetime64[ns]', freq='D')

print(a)
#                    A         B         C         D        
# 2016-07-01  0.240204  0.219076 -0.491247 -2.150830        
# 2016-07-02  0.356135 -1.033231  0.113561 -0.067777        
# 2016-07-03 -0.020235 -1.853201  1.433136 -1.452696        
# 2016-07-04 -0.206605  0.249365  0.233459 -1.751963        
# 2016-07-05 -0.710007 -0.827810  1.201611  0.029648        
# 2016-07-06  0.098759  0.306646  1.400452 -0.198219  


# np.nan : NaN값을 의미
a['F'] = [1.0, np.nan, 3.5, 6.1, np.nan, 7.0]
print(a)
#                    A         B         C         D    F   
# 2016-07-01 -0.442527  1.880417  0.943151  0.176536  1.0   
# 2016-07-02  0.232198  1.285691 -0.231192 -1.955863  NaN   
# 2016-07-03  0.226656  0.122844  0.372466 -1.064952  3.5   
# 2016-07-04 -1.027437 -0.659815 -1.719017 -0.793265  6.1   
# 2016-07-05  0.994993 -0.525990 -1.707228  0.543623  NaN   
# 2016-07-06  2.126898  2.522641 -0.842400  0.439097  7.0   


# Nan 없애기
# 행의 값중 하나라도 NaN인 경우 그 행을 없앤다.
print(a.dropna(how='any'))
#                    A         B         C         D    F   
# 2016-07-01 -1.494569 -0.360719  0.945333  0.931835  1.0   
# 2016-07-03 -0.231353 -0.409348 -0.942333  1.489558  3.5   
# 2016-07-04  1.539593 -1.676031 -2.888195 -0.556386  6.1   
# 2016-07-06 -2.943839  0.167685 -0.328562  0.623930  7.0   


# 행의 값의 모든 값이 NaN인 경우 그 행을 없앤다.
print(a.dropna(how='all'))
#                    A         B         C         D    F   
# 2016-07-01 -1.137907 -1.441493 -0.817488 -0.158701  1.0   
# 2016-07-02 -0.213143 -0.978253  0.229268  0.949477  NaN   
# 2016-07-03  0.533111  0.090548 -0.259886  1.705197  3.5   
# 2016-07-04 -0.410944  0.318927 -2.344918  0.477839  6.1   
# 2016-07-05  0.381804 -0.500594  0.369698 -1.011424  NaN   
# 2016-07-06 -1.584360 -0.132613  0.233714  1.368470  7.0  


print(a)
# *주의 : drop함수는 특정 행 or 열을 drop하고 난 DataFrame을 반환
#       : 즉, 반환을 받지 않으면 지돈의 DataFrame은 그대로 이다.
#                   A         B         C         D    F   
# 2016-07-01  0.073522  0.582794 -0.617488  0.351067  1.0   
# 2016-07-02  0.311803  1.831444 -0.453226  1.517955  NaN   
# 2016-07-03  0.101983  1.334711 -0.079788  0.223373  3.5   
# 2016-07-04 -0.605266 -1.855657 -1.012124  1.332695  6.1   
# 2016-07-05 -0.698066 -0.381208 -0.729591 -0.968811  NaN   
# 2016-07-06 -1.265256 -0.774155  0.686763  1.875213  7.0 

# 'inplace = True' 인자를 추가하여
# 반환을 받지 않고서도 기존의 DataFrame이 변경되도록 한다.


# NaN 값에 값 넣기
print(a.fillna(value = 0.5))
#                    A         B         C         D    F   
# 2016-07-01 -0.667990  1.730145  1.405912  0.791107  1.0   
# 2016-07-02  0.148199 -0.083202 -1.055864 -1.034010  0.5   
# 2016-07-03 -1.115853 -2.671121 -0.993976 -0.606761  3.5   
# 2016-07-04 -0.286785 -0.644467 -0.174597  0.048777  6.1   
# 2016-07-05  1.098337 -2.060713  0.115663  0.180972  0.5   
# 2016-07-06 -0.217733  1.310104 -0.342403  1.980473  7.0  



# NaN값인지 확인하기

