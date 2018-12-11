from LSTM_Worker.BitcoinUtil2 import get_bitcoin_data
import numpy as Numpy

lengthOfWindow = 1
lengthOfPrediction = 1


def prepare_testing_input_data(testing_data):
    Testing_LSTM_inputs = []
    for input in range(len(testing_data) - lengthOfWindow+1):
        store_data = testing_data[ input :( input + lengthOfWindow)].copy()
        Testing_LSTM_inputs.append(store_data)

    Testing_LSTM_inputs = [Numpy.array(Testing_LSTM_input) for Testing_LSTM_input in Testing_LSTM_inputs]
    Testing_LSTM_inputs = Numpy.array(Testing_LSTM_inputs)
    return Testing_LSTM_inputs


def split_data(bitcoin_data):
    date_splt = '2018-01-01'
    training_data = bitcoin_data
    testing_data = bitcoin_data[bitcoin_data['Date'] >= date_splt]
    training_data = training_data.drop('Date', 1)
    testing_data = testing_data.drop('Date', 1)
    return training_data, testing_data


def prepare_training_input_data(training_data):
    Training_LSTM_inputs = []
    for input in range(len(training_data) - lengthOfWindow+1):
        store_data = training_data[ input :( input + lengthOfWindow)].copy()
        Training_LSTM_inputs.append(store_data)
    #print(Training_LSTM_inputs[0])
    Training_LSTM_inputs = [Numpy.array(Training_LSTM_input) for Training_LSTM_input in Training_LSTM_inputs]
    Training_LSTM_inputs = Numpy.array(Training_LSTM_inputs)
    print(Training_LSTM_inputs.shape)
    return Training_LSTM_inputs


def prepare_training_output_data(training_data):
    Training_LSTM_outputs = []
    for input in range(lengthOfWindow, len(training_data['bt_Close**']) - lengthOfPrediction+1):
        Training_LSTM_outputs.append((training_data['bt_Close**'][input:input + lengthOfPrediction].values/
                                      training_data['bt_Close**'].values[input - lengthOfWindow]) - 1)
    Training_LSTM_outputs = Numpy.array(Training_LSTM_outputs)
    return Training_LSTM_outputs


def prepare_testing_output_data(testing_data):
    Testing_LSTM_outputs = []
    for input in range(lengthOfWindow, len(testing_data['bt_Close**']) - lengthOfPrediction+1):
        Testing_LSTM_outputs.append((testing_data['bt_Close**'][input:input + lengthOfPrediction].values /
                                     testing_data['bt_Close**'].values[input - lengthOfWindow]) - 1)
    Training_LSTM_outputs = Numpy.array(Testing_LSTM_outputs)
    return Training_LSTM_outputs


def set_win_pred_len(wind,pred):
    global lengthOfPrediction
    lengthOfPrediction = pred
    global lengthOfWindow
    lengthOfWindow = wind


def get_data(win_len,pred_len):
    set_win_pred_len(win_len,pred_len)
    extracted_data = get_bitcoin_data()
    training_data, testing_data = split_data(extracted_data)
    Training_LSTM_inputs = prepare_training_input_data(training_data)
    Training_LSTM_outputs = prepare_training_output_data(training_data)
    Testing_LSTM_inputs = prepare_testing_input_data(testing_data)
    Testing_LSTM_outputs = prepare_testing_output_data(testing_data)
    return Training_LSTM_inputs,Training_LSTM_outputs,Testing_LSTM_inputs,Testing_LSTM_outputs


if __name__ == '__main__':
    Training_LSTM_inputs, Training_LSTM_outputs, Testing_LSTM_inputs,Testing_LSTM_outputs = get_data(100,3)
    print("training input data")
    print(Training_LSTM_inputs.shape)
    print("training output data")
    print(Training_LSTM_outputs.shape)
    print("testing input data")
    print(Testing_LSTM_inputs.shape)
    print("testing output data")
    print(Testing_LSTM_outputs.shape)




