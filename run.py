from flask import render_template
from flask import Flask
from datetime import date
from datetime import timedelta
from pickle import load
app = Flask(__name__)

data = load(open("LSTM_Worker\predictdata.pkl","rb"))

future_dates = []
future_dates.append((date.today()).strftime("%b %d,%Y"))
future_dates.append((date.today()+timedelta(1)).strftime("%b %d, %Y"))
future_dates.append((date.today()+timedelta(2)).strftime("%b %d, %Y"))
future_prices = data[0]

past_dates = []
past_dates.append((date.today()-timedelta(1)).strftime("%b %d,%Y"))
past_dates.append((date.today()-timedelta(2)).strftime("%b %d, %Y"))
past_dates.append((date.today()-timedelta(3)).strftime("%b %d, %Y"))
past_predicted_prices = data[1]
past_actual_prices = data[2]

@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/predict',methods = ['POST', 'GET'])
def predict():
    return render_template('predict.html',dates=future_dates,prices=future_prices)

@app.route('/compare',methods = ['POST', 'GET'])
def compare():
    return render_template('compare.html',dates=past_dates,predict=past_predicted_prices,actual=past_actual_prices)

if __name__ == '__main__':
   app.run(debug=True)