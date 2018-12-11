from LSTM_Worker.BitcoinUtils import get_data
from LSTM_Worker.LSTM_Model import LSTM_Model
import numpy as Numpy
from keras.models import load_model

window_len = 1
prediction_range = 1
bitcoin_model = None


def get_parametrs():
    return window_len,prediction_range


def train_model():
    global bitcoin_model
    Training_LSTM_inputs, Training_LSTM_outputs, Testing_LSTM_inputs,Testing_LSTM_outputs = get_data(window_len,prediction_range)
    Numpy.random.seed(202)
    lstm = LSTM_Model(50,Training_LSTM_inputs,prediction_range)
    bitcoin_model = lstm.model_building()
    print(bitcoin_model.summary())
    print("Training of LSTM model starting :-")
    bitcoin_model.fit(Training_LSTM_inputs[:-prediction_range], Training_LSTM_outputs,
                      epochs=20, batch_size=1, verbose=2, shuffle=True)
    bitcoin_model.save('LSTModel.h5')


if __name__ == '__main__':
    train_model()
