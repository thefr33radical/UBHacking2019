
import pandas as pd
import datetime
from matplotlib import pyplot as plt
import requests
import io
from sklearn.metrics import mean_squared_error as rms
import numpy as np
import math 
import os
import helper


present_dir=os.path.dirname(os.path.abspath(__file__))
# XGboost regressor
# Random Forest Regressor
# LSTM
# Conv LSTM

# Interpretebility using lime

class Models(object):
    def __init__(self,path):        
        data = pd.read_csv(present_dir+path, error_bad_lines=False,header=0, parse_dates=[1], index_col=0, squeeze=True)
        data["Adj Close"] = data["Adj Close"].astype(float)
        self.multi_data=data
        data=data.loc[:,"Adj Close"]
        data=data[:100]
        self.uni_data=pd.Series(data)
        
    def ret_uni_data(self):        
        plt.figure(num=None, figsize=(20, 2), dpi=100,facecolor='w', edgecolor='k')
        plt.plot(self.uni_data.index,self.uni_data["Adj Close"],marker='*', color='maroon')
        plt.show()        

    def uni_baseline(self,steps):
        pred_values=[]

        end =int(0.2*len(self.uni_data))
        values = self.uni_data[:-end]
        actual_values = self.uni_data[len(self.uni_data)-end:]
        pred_values=[]
        indexes=self.uni_data[len(self.uni_data)-end:].index

        for i in range(1,len(actual_values)):
            pred_values.append(actual_values[i])
            
        pred_values.append(0)
        
        """plt.figure(num=None, figsize=(20, 2), dpi=100,facecolor='w', edgecolor='k')
        plt.xlabel('Time', fontsize=8)
        plt.ylabel('Adjusted Stock ', fontsize=8)
        plt.plot(actual_values,marker='.', color='pink')
        plt.plot(pred_values,marker='.', color='purple')
        plt.title("Adjusted Stocks ",fontsize=12)
        plt.show()
        """

        rmse=math.sqrt(rms(actual_values,pred_values))
        print("RMSE VALUE : ",rmse)
        return { "model":"Baseline","index":list(indexes), "actual":list(actual_values.values), "predicted":list(pred_values),"rmse":rmse}
         
    def uni_sarima(self,steps):
        return helper.sarima(self.uni_data,steps)
        pass

    def uni_arima_ann(self,steps):
        pass

    def multi_elasticnet(self,steps):
        pass

    def prophet(self,steps):
        end =int(0.2*len(self.multi_data))
        values = self.multi_data[:-end]
        m= Prophet()
        m.fit(values)
        actual_values = self.uni_data[len(self.multi_data)-end:]

        future = m.make_future_dataframe(periods=len(self.multi_data)-end)
        forecast = m.predict(future)
        print(forecast[self.multi_data.columns].tail())        

    def lstm(self,steps):
        return helper.lstm(self.uni_data,steps)

    def multi_cnn_lstm(self,steps):
        pass

if __name__=="__main__":
    steps=10
    obj=Models("\data\data_ub.csv")
    #obj.uni_baseline(steps)
    #obj.uni_sarima(steps)
    #obj.prophet(steps)
    obj.lstm(steps)
    

    
