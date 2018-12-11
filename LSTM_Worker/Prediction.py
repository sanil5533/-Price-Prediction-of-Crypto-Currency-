from LSTM_Worker.PredictionUtils import getPredictionData
from keras.models import load_model
from LSTM_Worker.TrainModel import get_parametrs
from pickle import dump,load
from datetime import  date
window_len, prediction_range = get_parametrs()

tmp = load(open('date.pkl','rb'))
if tmp == date.today():
    future_list, future_set, past_list, past_set, past_actual = getPredictionData(window_len, prediction_range)
    data = [future_list,future_set,past_list,past_set,past_actual]
    dump(data,open('ipdata.pkl','wb'))
else:
    data = load(open('ipdata.pkl','rb'))
    future_list=data[0]
    future_set=data[1]
    past_list=data[2]
    past_set=data[3]
    past_actual=data[4]

def predictPast():
    global future_list, future_set, past_list, past_set, past_actual
    bitcoin_model = load_model('LSTMmodel.h5')
    pas  = bitcoin_model.predict(past_list).reshape(prediction_range)
    pas = pas + 1
    pas = pas * past_set['bt_Close**'].values[0].reshape(1)
    #print("pas= "+str(pas))
    fut = bitcoin_model.predict(future_list).reshape(prediction_range)
    fut = fut + 1
    fut = fut * future_set['bt_Close**'].values[0].reshape(1)
    #print("future= "+str(fut))
    data = []
    data.append(fut)
    data.append(pas)
    data.append(past_actual)
    dump(data, open("..\predictdata.pkl", "wb"))

if __name__=="__main__":
    predictPast()