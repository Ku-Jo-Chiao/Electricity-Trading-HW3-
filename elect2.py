# -*- coding: utf-8 -*-
"""elect2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1AuMKlvT6vkDfuJnaNkPb_it3U3v9rBTF
"""



import os
file_path = './training_data/'
allFileList = os.listdir(file_path)
import csv
time = []
gen = []
con = []
sur = []
for file in allFileList:
  with open(file_path + file, newline='') as csvfile:
    rows = csv.reader(csvfile)
    for row in rows:
      try:
        #time.append(row[0])
        gen.append(float(row[1]))   #generation
        con.append(float(row[2]))   #consumption
        sur.append([float(row[1]) - float(row[2])])   #generation-consumption
      except:
        pass

print('gen: ' + str(len(gen)))
print('con: ' + str(len(con)))
print('sur: ' + str(len(sur)))
print(sur[0])

import matplotlib.pyplot as plt

xpt=range(1,len(sur))
plt.scatter(range(1,len(sur)+1), sur, s=15, c='blue')
plt.title("Sur Power", fontsize=24) #圖表標題
plt.xlabel("Times", fontsize=16) #x軸標題
plt.ylabel("Power(gen-con)", fontsize=16) #y軸標題
plt.savefig('data_original.png')
plt.show() #顯示繪製的圖形

import numpy
import pandas as pd 
from sklearn.preprocessing import RobustScaler
import numpy as np
sur = np.array(sur)
robust_scaler = RobustScaler()
RS_sur = robust_scaler.fit_transform(sur)
print(RS_sur)
plt.scatter(range(1,len(RS_sur)+1), RS_sur, s=15, c='orange')
plt.title("RS Sur Power", fontsize=24) #圖表標題
plt.xlabel("Times", fontsize=16) #x軸標題
plt.ylabel("Power(gen-con)", fontsize=16) #y軸標題
plt.savefig('data_robust.png')
plt.show()
pd.DataFrame(RS_sur).to_csv("./RS_sur.csv")

"""## 建立模型"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import matplotlib
# get data
import pandas_datareader as pdr

# visual
import matplotlib.pyplot as plt

# %matplotlib inline
import seaborn as sns

#time
import datetime as datetime

from keras.models import Sequential

from keras.layers import Dense, Dropout, Activation, Flatten, LSTM, TimeDistributed, RepeatVector, GRU, BatchNormalization
from keras import regularizers
from keras.callbacks import EarlyStopping
import numpy as np
import tensorflow as tf

pd.__version__

train_data = pd.read_csv("./RS_sur.csv")
train_data.columns=["Number", "RS"]
train_data = train_data.drop(columns=["Number"])
train_data = train_data.iloc[-24:] #讀最後24條
train_data = train_data.reset_index(drop=True)#刪除索引
train_data.columns = [''] * len(train_data.columns)
train_data.head(7)
print(train_data)
save_data = train_data.to_csv("./RS_forpredict.csv",index = False)#儲存為不帶索引的csv

def readTrain():
  train = pd.read_csv("./RS_sur.csv")
  train.columns=["Number", "RS"]
  train = train.drop(columns=["Number"])  #拿掉第一行
  return train



#建立訓練data
def buildTrain(train,pastDay,futureDay):
    X_train, Y_train = [], []
    for i in range(train.shape[0]-futureDay-pastDay):
      X_train.append(np.array(train.iloc[i:i+pastDay])) #分割訓練集      
      Y_train.append(np.array(train.iloc[i+pastDay:i+pastDay+futureDay]["RS"])) #分割輸出label
    return np.array(X_train), np.array(Y_train)
#分割data
def splitData(X,Y,rate):
  X_train = X[int(X.shape[0]*rate):]
  
  Y_train = Y[int(Y.shape[0]*rate):]
  X_val = X[:int(X.shape[0]*rate)]

  Y_val = Y[:int(Y.shape[0]*rate)]
  return X_train, Y_train, X_val, Y_val

# read SPY.csv
train = readTrain()



# build Data, use last 168 hours to predict next 24 days
X_train, Y_train, = buildTrain(train,24, 24)

# split training data and validation data
X_train, Y_train,X_val, Y_val,  = splitData(X_train, Y_train, 0.1)
print(X_train.shape)
print(Y_train.shape)

def buildManyToManyModel(shape):

  model = Sequential()
  #一個特徵
  model.add(LSTM(16, input_length=shape[1], input_dim=shape[2], return_sequences=True))
  model.add(Dropout(0.2))
  model.add(LSTM(8, input_length=shape[1], input_dim=shape[2], return_sequences=True))
  model.add(Dropout(0.2))
  model.add(LSTM(1, input_length=shape[1], input_dim=shape[2], return_sequences=True))
  model.add(TimeDistributed(Dense(1)))
  model.compile(loss="mse", optimizer="adam")
  model.summary()
  return model

def buildManyToManyModel_2(shape):

  model = Sequential()
  #一個特徵
  model.add(LSTM(8, input_length=shape[1], input_dim=shape[2], return_sequences=True, kernel_regularizer=regularizers.l2(0.0001)  ))
  model.add(Dropout(0.2))
  model.add(LSTM(4, input_length=shape[1], input_dim=shape[2], return_sequences=True, kernel_regularizer=regularizers.l2(0.0001) ))
  model.add(Dropout(0.2))
  model.add(LSTM(1, input_length=shape[1], input_dim=shape[2], return_sequences=True, kernel_regularizer=regularizers.l2(0.0001) ))
  model.add(TimeDistributed(Dense(1)))
  model.compile(loss="mse", optimizer="RMSprop")
  model.summary()
  return model

def buildManyToManyModel_3(shape):

  model = Sequential()
  #一個特徵
  model.add(GRU(32, input_length=shape[1], input_dim=shape[2], return_sequences=True, kernel_regularizer=regularizers.l2(0.0001)  ))
  model.add(BatchNormalization())
  model.add(Dropout(0.5))
  model.add(GRU(16, input_length=shape[1], input_dim=shape[2], return_sequences=True, kernel_regularizer=regularizers.l2(0.0001)  ))
  model.add(BatchNormalization())
  model.add(Dropout(0.2))
  model.add(GRU(1, input_length=shape[1], input_dim=shape[2], return_sequences=True, kernel_regularizer=regularizers.l2(0.0001)  ))
  model.add(TimeDistributed(Dense(1)))
  model.compile(loss="mse", optimizer="RMSprop")
  model.summary()
  return model


train = readTrain()

# change the last 168 hours  and next 24 hours 
X_train, Y_train= buildTrain(train, 24, 24)

X_train, Y_train, X_val, Y_val= splitData(X_train, Y_train, 0.1)


model = buildManyToManyModel_3(X_train.shape)
callback = EarlyStopping(monitor="loss", patience=10, verbose=1, mode="auto")

history=model.fit(X_train, Y_train, epochs=30, batch_size=64, validation_data=(X_val, Y_val), callbacks=[callback])

import matplotlib.pyplot as plt
fig = plt.figure()
plt.plot(history.history['loss'],label='training loss')
plt.plot(history.history['val_loss'], label='val loss')
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(loc='upper right')
fig.savefig('./RS_gru.png')

model.save('./RS_gru.h5')

"""開始預測"""

#---------------預測未來二十四小時------------------
from tensorflow.keras.models import load_model
model_close = load_model('./RS_gru.h5')
predict_data = pd.read_csv('./RS_forpredict.csv', names=["RS"])
predict_data = predict_data.drop([0])
#print(predict_data)

#---------------電量------------------

#Build data for predict
close_predict = []
def buildpredict_close(data):        
    close_predict.append(np.array(data.iloc[0:24]))
    return np.array(close_predict)

# build Data, use last 7 days to predict next 1 days
close_predict_data = buildpredict_close(predict_data)


prediction_close = model_close.predict(close_predict_data)

#2D:1*20
prediction_close_reshape=np.reshape(prediction_close,(prediction_close.shape[0],prediction_close.shape[1]))

#1D:20
sub_close=prediction_close_reshape[-1]
#numpy.ndarry to dataframe
dfs_close= pd.DataFrame(sub_close)

prediction_array=dfs_close.to_numpy()
print(prediction_array)