import requests, ast
import pandas as pd
from datetime import date
import time

def fetch_exchange_rate(currency, date):
    if currency == 'pln':
        return 1
    url = 'https://api.nbp.pl/api/exchangerates/rates/a/'
    response = requests.get(url + str(currency) + "/" + str(date))
    res_dict = ast.literal_eval(response.content.decode()) #converting response to dictionary
    return res_dict['rates'][0]['mid']
    
def read_and_join_data(liability_path, payment_path):
    liability = pd.read_csv(liability_path,index_col=0)
    payment = pd.read_csv(payment_path,index_col=0)
    result = liability.join(payment)
    result['payment value'] = result['payment value'].fillna(0)
    result['payment date'] = result['payment date'].fillna(result['liability date'])
    return result

def calculate_balance(data, result_path):
    today = str(date.today())
    liability_exchange_rate = [fetch_exchange_rate(data.loc[i,'currency'],
                                            data.loc[i,'liability date']) 
                                            for i in data.index]
    payment_exchange_rate = [fetch_exchange_rate(data.loc[i,'currency'],
                                            data.loc[i,'payment date']) 
                                            for i in data.index]
    today_exchange_rate = [fetch_exchange_rate(data.loc[i,'currency'],
                                            today) 
                                            for i in data.index]
    data['original exchange rate'] = liability_exchange_rate
    data['payment exchange rate'] = payment_exchange_rate
    data['today exchange rate'] = today_exchange_rate
    data['original value in pln'] = data['liability value']*liability_exchange_rate
    data['paid value in foreign'] = data['payment value']/payment_exchange_rate
    data['remaining liability in foreign'] = data['liability value'] - data['paid value in foreign']
    data['remaining liability in pln'] = data['remaining liability in foreign']*today_exchange_rate

    data.to_csv(result_path)
    return data

if __name__ == '__main__':
    liability_path = 'liabilities_big.csv'
    payment_path = 'payments_big.csv'
    result_path = 'summary_big.csv'

    start = time.time()
    df = read_and_join_data(liability_path,payment_path)
    result = calculate_balance(df, result_path)
    end = time.time()
    print(result)
    print('Execution time: ', (end-start), 's')