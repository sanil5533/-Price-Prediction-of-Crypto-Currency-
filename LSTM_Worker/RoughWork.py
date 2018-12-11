import pandas as Panda
from keras.models import load_model

data = Panda.read_csv('bitcoinData.csv')
#print(data)

prev_model = load_model('LSTMmodel.h5')

print(prev_model.optimizer)
print(prev_model.get_weights())