
from statsmodels.tsa.api import ExponentialSmoothing, SimpleExpSmoothing, Holt, SARIMAX
import pandas as pd
import datetime
from matplotlib import pyplot as plt
import requests
import io
from sklearn.metrics import mean_squared_error as rms
import numpy as np
from statsmodels.tsa.arima_model import ARIMA


def sarima(data,steps):
    model=SARIMAX(endog=data.values,order=(2,0,1),seasonal_order=(0,1,1,7),enforce_invertibility=False)
    sarima_fit= model.fit()
    print(sarima_fit.summary())

    # Rollling Forecast

        
    # Number of days to Forecast Parameter
    end =7
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
    plt.figure(num=None, figsize=(10, 2), dpi=100,facecolor='w', edgecolor='k')
    plt.xlabel('Time', fontsize=8)
    plt.ylabel('Inpatients', fontsize=8)
    plt.plot(actual_values,marker='.', color='pink')
    plt.plot(pred_values,marker='.', color='purple')
    plt.title("Inpatients Prediction Forecast",fontsize=12)
    plt.show()

    # Needs correction ??
    print("RMSE VALUE",math.sqrt(rms(actual_values,pred_values)))
    #print(actual_values,pred_values)