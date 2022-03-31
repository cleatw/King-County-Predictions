# -*- coding: utf-8 -*-
# Import general libraries
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import statistics

# importing relevant library
from statsmodels.tsa.stattools import adfuller
from sklearn.metrics import mean_squared_error
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.graphics.tsaplots import plot_acf

# For testing stationarity
def dicky_fuller_test(data, alpha):
    is_stationary = adfuller(data)[1] < alpha
    if is_stationary == True:
        print(f'The data is stationary with a fuller score of {round(adfuller(data)[1],3)}')
    else:
        print(f'The data is not stationary with a fuller score of {round(adfuller(data)[1],3)}')
    return


# Defining a function to pop things from a list.
def without(lst, idx):
    return [x for i, x in enumerate(lst) if i != idx]


def format_df(df):
    # Creating function to melt dataframes and set time-date index
    #      - To use this function your dataframe must be in wide format 
    #        with your first column as your intended columns.
    #      - IE, your dataframe should look like this:
    #       =====================================================
    #       =      = Cities = 1996-01 = 1996-02 = 1996-03 = ... = 
    #       =====================================================
    #       =      = Dallas = 334200. = 123456. = 123525. = ... =
    #       =      = Austin = 235700. = 123456. = 123552. = ... =
    #       =      = San A* = 500900. = 123456. = 123235. = ... =
    #       =      = Porch  = 1287700 = 1234567 = 123123. = ... =
    #       = ...  =
    #       =      = Katy   = 235700. = 12345.0 = 1231.01 = ... =
    #       =      = McKin* = 235700. = 123445. = 123456. = ... =
    #       =      = El Pa* = 1287700 = 1234565 = 1234512 = ... =
    #       =====================================================

    test_list = pd.melt(df, id_vars = df.columns.to_list()[:1], var_name='Date')
    test_list['Date'] = pd.to_datetime(test_list['Date'], infer_datetime_format=True)
    test_list = test_list.dropna(subset=['value'])
    test_list.groupby('Date').aggregate({'value':'mean'})
    return test_list.pivot_table(index='Date', columns=df.columns.to_list()[:1], values='value')



def stationizer(df, window, alpha=0.05, verbose=True):
    # This function takes a formatted dataframe from format_df(), a window for the rolling mean 
    # and an alpha for a dicky fuller test and performs two transformations:
    #
    # 1. The dataframe's rolling average is subtracted from the dataframe and a fuller score is printed.
    #
    # 2. A difference is performed on the dataframe resulting from step 1 and a fuller score is printed.
    #
    # The function returns the transformed dataframe. If the steps prior are sufficient to make a stationary
    # series, the function will return the dataframe that is sufficiently stationary.
    
    df1 = df - df.rolling(window=window).mean().dropna()
    df2 = df1.diff().dropna()
    df3 = df.diff().dropna()
    df4 = df.diff().diff().dropna()
    
    if verbose == True:
        print(f'Before transformations:')
        dicky_fuller_test(df.dropna(), alpha)
        print(f'After subtracting rolling mean:')
        dicky_fuller_test(df1.dropna(), alpha)
        print(f'After differencing:')
        dicky_fuller_test(df2.dropna(), alpha)
        print('With only differencing:')
        dicky_fuller_test(df3.dropna(), alpha)
        print('With differencing twice:')
        dicky_fuller_test(df4.dropna(), alpha)
    
    if adfuller(df)[1] < alpha:
        return df
    elif adfuller(df1.dropna())[1] < alpha:
        return df1
    elif adfuller(df3.dropna())[1] < alpha:
        return df3
    elif adfuller(df2.dropna())[1] < alpha:
        return df2
    else:
        return df4
        


def get_qroi(d):
    # This function returns the dataframe with quartarly ROI values for a given set of price in series.
    
    return (d.rolling(window = 3).max() - d.rolling(window = 3).min()) / d.rolling(window = 3).min()



def get_na(df):
    # This function checks for null values by column
    
    for i in df.columns:
        if df[i].isna().value_counts().tolist()[0] != df.shape[0]:
            print(f'{i} has null values')
    pass


def fix_na(df):
    # interpolate and backfill
    
    df = df.interpolate(method='linear').fillna(value=None, method='backfill', axis=None, limit=None, downcast=None).dropna(axis=1, how='all')
    return df



def plot(df):
    # For plotting time series
    
    df.plot(figsize=(14,6), linewidth=2, fontsize=14, rot= 45)
    pass


def Multi_ARIMA(train, test, order=(1,0,0), plot = False):
    # performs an ARIMA model on each column of the dataset 
    # and returns the mean RMSE from a walk-forward validation
    from statistics import mean
    rmse_list = []
    for i in train.columns:
        x_train = train[i]
        x_test = test[i]
        
        predictions = []
        history = [x for x in x_train]
        
        # walk-forward validation
        for t in range(len(test)):
            model = ARIMA(history, order=order)
            model_fit = model.fit()
            output = model_fit.forecast()
            yhat = output[0]
            predictions.append(yhat)
            obs = x_test[t]
            history.append(obs)
        #   print('predicted=%f, expected=%f' % (yhat, obs))
            
        if plot == True:
            # plot forecasts against actual outcomes
            x_predictions = pd.DataFrame(predictions)
            x_predictions = x_predictions.set_index(test.index)
            plt.plot(x_test)
            plt.plot(x_predictions, color='red')
            plt.xticks(rotation = 45) # Rotates X-Axis Ticks by 45-degrees
            plt.title(f'ROI for {i}')
            plt.legend(loc='upper left', fontsize=8)
            plt.show()
            print(f'RMSE: {mean_squared_error(x_test, predictions, squared=False)}')
    
        # evaluate forecasts
        rmse_list.append(mean_squared_error(x_test, predictions, squared=False))
    return mean(rmse_list),

def set_index(df, date_column):
    # Sets time series index
    return df.set_index(pd.to_datetime(df[date_column])).drop(columns=date_column)

