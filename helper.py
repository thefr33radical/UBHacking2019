
from statsmodels.tsa.api import ExponentialSmoothing, SimpleExpSmoothing, Holt, SARIMAX
import pandas as pd
import datetime
from matplotlib import pyplot as plt
import requests
import io
from sklearn.metrics import mean_squared_error as rms
import numpy as np
from statsmodels.tsa.arima_model import ARIMA
import math
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM

def sarima(data,steps):
    model=SARIMAX(endog=data.values,order=(2,0,1),seasonal_order=(0,1,1,7),enforce_invertibility=False)
    sarima_fit= model.fit()
    print(sarima_fit.summary())

    # Rollling Forecast
        
    # Number of days to Forecast Parameter
    end =int(0.2*len(data))
    values = data[:-end]
    actual_values = data[len(data)-end:]
    pred_values=[]
    indexes=data[len(data)-end:].index

    for i in range(end):
        model = ARIMA((values),(2, 0, 1))
        arima_fit= model.fit()
        
        fnext = arima_fit.forecast()[0][0] 
        pred_values.append(fnext)
        values = data[:-end+i]

    pred_values=pd.Series(pred_values)
    pred_values.index=indexes

    #Doubt
    #pred_values=pred_values.shift(-1)[:]
    """
    plt.figure(num=None, figsize=(10, 2), dpi=100,facecolor='w', edgecolor='k')
    plt.xlabel('Time', fontsize=8)
    plt.ylabel('Inpatients', fontsize=8)
    plt.plot(actual_values,marker='.', color='pink')
    plt.plot(pred_values,marker='.', color='purple')
    plt.title("Inpatients Prediction Forecast",fontsize=12)
    plt.show()
    """
    rmse=rms(actual_values,pred_values)
    # Needs correction ??
    print("RMSE VALUE",rmse)
    #print(actual_values,pred_values)
    print(len(pred_values))
    return { "model":"Baseline","index":list(indexes), "actual":list(actual_values.values), "predicted":list(pred_values),"rmse":rmse}

def transform_supervised(dat,lag=1):
    x=dat.shift(lag)
    y=dat
    return x,y  

def scale_data(df):
    mx=MinMaxScaler()
    df["x"]=mx.fit_transform(np.asarray(df["x"]).reshape(-1,1))
    return mx,df  

def inverse_scale_data(mx,df):
    df["x"]=mx.inverse_transform(np.asarray(df["x"]).reshape(-1,1))
    return mx,df  

def fit_lstm(df, batch_size, nb_epoch, neurons):
  x, y = df.iloc[:,:-1], df.iloc[:, -1]
  x = np.asarray(x).reshape(x.shape[0], 1, x.shape[1])
  model = Sequential()
  model.add(LSTM(neurons, batch_input_shape=(batch_size, x.shape[1], x.shape[2]), stateful=True))
  model.add(Dense(1))
  model.compile(loss='mean_squared_error', optimizer='adam')
  for i in range(nb_epoch):
    model.fit(x, y, epochs=1, batch_size=batch_size, verbose=0, shuffle=False)
    model.reset_states()
  return x,model

def lstm(data,steps):
    indexes=data.index
    end =int(0.2*len(data))
    train, test = data[0:-end], data[-end:]

    x,y=transform_supervised(train)

    df = pd.concat([x,y],axis=1)
    df.columns=["x","y"]
    df.fillna(0,inplace=True)
    mx,df=scale_data(df)

    x,lstm_model = fit_lstm(df, 1, 5, 40)
    # forecast the entire training dataset to build up state for forecasting
    #train_reshaped = train_scaled[:, 0].reshape(len(train_scaled), 1, 1)
    testx,testy=transform_supervised(test)

    df1 = pd.concat([testx,testy],axis=1)
    df1.columns=["x","y"]
    df1.fillna(0,inplace=True)
    mx1,df1=scale_data(df1)
    testx, testy = df1.iloc[:,:-1], df1.iloc[:, -1]
    testx = np.asarray(testx).reshape(testx.shape[0], 1, testx.shape[1])

    pred_values = lstm_model.predict(testx, batch_size=1)
    
    rmse=rms(testy,pred_values)
    print("RMSE VALUE : ",rmse)
    return { "model":"Baseline","index":indexes[-end:], "actual":testy, "predicted":pred_values,"rmse":rmse}
