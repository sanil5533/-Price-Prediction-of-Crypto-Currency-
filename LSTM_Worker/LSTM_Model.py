from keras.layers import LSTM
from keras.layers import Activation, Dense
from keras.layers import Dropout
from keras.models import Sequential
import numpy as Numpy

class LSTM_Model:
    noOfneurons = None
    input_data = None
    size_output = None
    loss_value = "mae"
    dropout_value = 0.25
    activation_function = "tanh"
    optmzr = "adam"

    def __init__(self,neurons=50,input=Numpy.zeros((1650,100,7)),output_size=3):
        self.noOfneurons = neurons
        self.input_data = input
        self.size_output = output_size

    def model_building(self):
        classifier = Sequential()
        classifier.add(LSTM(self.noOfneurons, return_sequences=True, input_shape=(self.input_data.shape[1], self.input_data.shape[2])))
        classifier.add(Dropout(self.dropout_value))
        classifier.add(LSTM(self.noOfneurons, return_sequences=True))
        classifier.add(Dropout(self.dropout_value))
        classifier.add(LSTM(self.noOfneurons))
        classifier.add(Dropout(self.dropout_value))
        classifier.add(Dense(units=self.size_output))
        classifier.add(Activation(self.activation_function))
        classifier.compile(loss=self.loss_value, optimizer=self.optmzr)
        return classifier


if __name__ == '__main__':
    lstm = LSTM_Model()
    classifier = lstm.model_building()
    print("Model summary")
    print(classifier.summary())

