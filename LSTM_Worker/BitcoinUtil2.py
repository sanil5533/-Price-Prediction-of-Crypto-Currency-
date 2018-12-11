import pandas as Panda
from datetime import date
from datetime import timedelta
from pickle import dump, load

startday = "20140101"
endday = (date.today()-timedelta(1)).strftime("%Y%m%d")
url1 = "https://coinmarketcap.com/currencies/bitcoin/historical-data/?start="
url2 = "&end="
tmp = load(open('date.pkl','rb'))
if tmp == date.today():
    flag = 1
else:
    flag = 0
#flag = 0

def change_values(panda_data):
    panda_data = panda_data.assign(Date=Panda .to_datetime(panda_data['Date']))
    panda_data['Volume'] = panda_data['Volume'].astype('int64')
    return panda_data


def extract_data():
    global flag
    if flag == 0:
        try:
            url_bitcoin = url1 + startday + url2 + endday
            past_data_bitcoin = Panda.read_html(url_bitcoin)[0]
            print("Current bitcoin data is extracted")
        except Exception as e:
            print("Exception in fetching url : - " + str(e))
            past_data_bitcoin = None
            flag = 1
    else:
        past_data_bitcoin = None
    return past_data_bitcoin

def extract_features(bitpast_data):
    final_data = bitpast_data[['Date'] + ['bt_' + colmns for colmns in ['Close**', 'Volume', 'Supply','close_off_high','volatility','High','Low']]]
    final_data = final_data.sort_values(by='Date')
    return final_data


def rename_columns(bitcoin_data):
    bitcoin_data.columns = [bitcoin_data.columns[0]] + ['bt_' + col for col in bitcoin_data.columns[1:]]
    return bitcoin_data


def get_bitcoin_data():
    ext_data = extract_data()
    if flag == 0:
        chng_value = change_values(ext_data)
        rnm_columns = rename_columns(chng_value)
        supply = add_columns(rnm_columns)
        final_data = extract_features(supply)
        final_data.to_csv('bitcoinData.csv')
        dump(date.today(),open('date.pkl','wb'))
    else:
        print("Previous data extracted")
        final_data = Panda.read_csv('bitcoinData.csv')
        final_data = final_data.drop('Unnamed: 0',1)
    return final_data


def add_columns(bitcoin_data_info):
    temp = {'bt_Supply': lambda fd: (fd['bt_Market Cap']) / (fd['bt_Close**'])}
    bitcoin_data_info = bitcoin_data_info.assign(**temp)
    temp = {'bt_close_off_high': lambda fd: (2*(fd['bt_High']- fd['bt_Close**'])/(fd['bt_High']-fd['bt_Low'])-1)}
    bitcoin_data_info = bitcoin_data_info.assign(**temp)
    temp = {'bt_volatility': lambda fd: (fd['bt_High']- fd['bt_Low'])/(fd['bt_Open*'])}
    bitcoin_data_info = bitcoin_data_info.assign(**temp)
    return bitcoin_data_info


if __name__ == '__main__':
    final_panda_data = get_bitcoin_data()
    print("final panda Data frame :- ")
    print(final_panda_data.head())