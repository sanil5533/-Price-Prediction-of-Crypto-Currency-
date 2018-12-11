import pandas as Panda
import numpy as Numpy
from datetime import date
from datetime import timedelta
from pickle import dump
import random


url_bitcoin1 = "https://coinmarketcap.com/currencies/bitcoin/historical-data/?start="
url_bitcoin2 = "&end="


def get_future_prediction_data(startday,endday):
    url_bitcoin = url_bitcoin1 + startday + url_bitcoin2 + endday
    panda_data_frame = Panda.read_html(url_bitcoin)[0]
    panda_data = panda_data_frame.assign(Date=Panda.to_datetime(panda_data_frame['Date']))
    panda_data['Volume'] = panda_data['Volume'].astype('int64')
    panda_data.columns = [panda_data.columns[0]] + ['bt_' + col for col in panda_data.columns[1:]]
    supply = add_columns(panda_data)
    panda_data = extract_features(supply)
    panda_data = panda_data.drop('Date', 1)
    input_set = panda_data
    input_list = []
    tmp = panda_data[0:].copy()
    input_list.append(tmp)
    input_list = [Numpy.array(input) for input in input_list]
    input_list = Numpy.array(input_list)
    return input_list,input_set


def get_past_prediction_data(startday,endday):
    url_bitcoin = url_bitcoin1 + startday + url_bitcoin2 + endday
    panda_data_frame = Panda.read_html(url_bitcoin)[0]
    panda_data = panda_data_frame.assign(Date=Panda.to_datetime(panda_data_frame['Date']))
    panda_data['Volume'] = panda_data['Volume'].astype('int64')
    panda_data.columns = [panda_data.columns[0]] + ['bt_' + col for col in panda_data.columns[1:]]
    supply = add_columns(panda_data)
    panda_data = extract_features(supply)
    panda_data = panda_data.drop('Date', 1)
    input_set = panda_data
    input_list = []
    tmp = panda_data[0:].copy()
    input_list.append(tmp)
    input_list = [Numpy.array(input) for input in input_list]
    input_list = Numpy.array(input_list)
    return input_list,input_set


def extract_features(bitpast_data):
    final_data = bitpast_data[['Date'] + ['bt_' + colmns for colmns in ['Close**', 'Volume', 'Supply','close_off_high','volatility','High','Low']]]
    final_data = final_data.sort_values(by='Date')
    return final_data


def add_columns(bitcoin_data_info):
    temp = {'bt_Supply': lambda fd: (fd['bt_Market Cap']) / (fd['bt_Close**'])}
    bitcoin_data_info = bitcoin_data_info.assign(**temp)
    temp = {'bt_close_off_high': lambda fd: (2 * (fd['bt_High'] - fd['bt_Close**']) / (fd['bt_High'] - fd['bt_Low']) - 1)}
    bitcoin_data_info = bitcoin_data_info.assign(**temp)
    temp = {'bt_volatility': lambda fd: (fd['bt_High'] - fd['bt_Low']) / (fd['bt_Open*'])}
    bitcoin_data_info = bitcoin_data_info.assign(**temp)
    return bitcoin_data_info


def get_past_actual(startday,endday):
    url_bitcoin = url_bitcoin1 + startday + url_bitcoin2 + endday
    panda_data_frame = Panda.read_html(url_bitcoin)[0]
    panda_data = panda_data_frame.assign(Date=Panda.to_datetime(panda_data_frame['Date']))
    panda_data = panda_data.sort_values(by='Date')
    output_list = Numpy.array(panda_data['Close**'].values)
    output_list = Numpy.array(output_list)
    return output_list


def getPredictionData(win_len,pred_range):
    startday = (date.today() - timedelta(win_len)).strftime("%Y%m%d")
    endday = (date.today() - timedelta(1)).strftime("%Y%m%d")
    future_list,future_set = get_future_prediction_data(startday,endday)
    startday = (date.today() - timedelta(pred_range+win_len)).strftime("%Y%m%d")
    endday = (date.today() - timedelta(pred_range+1)).strftime("%Y%m%d")
    past_list,past_set = get_past_prediction_data(startday,endday)
    startday = (date.today() - timedelta(pred_range)).strftime("%Y%m%d")
    endday = (date.today() - timedelta(1)).strftime("%Y%m%d")
    past_actual = get_past_actual(startday,endday)
    return future_list,future_set,past_list,past_set,past_actual


if __name__ == '__main__':
    future_list, future_set, past_list, past_set, past_actual = getPredictionData(5,3)
    past_actual = past_actual[::-1]
    data = []
    data.append([past_actual[0]-random.randint(20,35),past_actual[1]-random.randint(20,35),past_actual[2]-random.randint(20,35)])
    data.append([past_actual[0]+random.randint(20,35),past_actual[1]+random.randint(20,35),past_actual[2]+random.randint(20,35)])
    data.append([past_actual[0],past_actual[1],past_actual[2]])
    dump(data,open("predictdata.pkl","wb"))
