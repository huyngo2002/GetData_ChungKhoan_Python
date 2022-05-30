import requests
import pandas as pd
import logging as logging
from datetime import datetime


def convert_date(text, date_type='%d/%m/%Y'):
    return datetime.strptime(text, date_type)

def convert_text_dateformat(text, origin_type = '%Y-%m-%d', new_type = '%Y-%m-%d'):
    return convert_date(text, origin_type).strftime(new_type)

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
class DataLoader:
    def __init__(self, symbols, start, end):
        self.symbols = symbols
        self.start = ''
        self.end = ''
        if start != '':
            self.start = convert_text_dateformat(start, new_type='%Y-%m-%d')
        if end != '':
            self.end = convert_text_dateformat(end, new_type='%Y-%m-%d')
    
    def download(self):
        stock_datas = []
        if not isinstance(self.symbols, list):
            symbols = [self.symbols]
        else:
            symbols = self.symbols
        
        for symbol in symbols:
            stock_datas.append(self.download_one(symbol))
        
        data = pd.concat(stock_datas, axis=1)

        return data

    def download_one(self, symbol):
        url = 'https://s.cafef.vn/ajax/bieudokythuat.ashx?symbol=' + symbol

        resp = requests.get(url)
        datas = resp.text.split('\n')
        index = datas[1].find('=')
        jsonData = datas[1][index + 1: -2]
        data = eval(jsonData)

        data = pd.DataFrame(data)
        if not data.empty:
            stock_data = data[['dateVN', 'close', 'Volume']].copy()
            stock_data.columns = ['date', 'close', 'volume']

            stock_data = stock_data.set_index('date').apply(pd.to_numeric, errors='coerce')
            stock_data.index = list(map(convert_date, stock_data.index))
            stock_data.index.name = 'date'
            stock_data = stock_data.sort_index()
            stock_data.fillna(0, inplace=True)

            if self.start != '' and self.end != '':
                # make boolean mask
                mask = (stock_data.index >= self.start) & (stock_data.index <= self.end)
                # Select the sub data frame
                stock_data = stock_data.loc[mask]

                logging.info('data {} from {} to {} have already cloned!' \
                     .format(symbol, self.start, self.end))
                            # convert_text_dateformat(self.start, origin_type = '%d/%m/%Y', new_type = '%Y-%m-%d'),
                            # convert_text_dateformat(self.end, origin_type='%d/%m/%Y', new_type='%Y-%m-%d')))
            else:
                logging.info('data {} have already cloned!' \
                     .format(symbol))
            
            # stock_data['date'] = stock_data['date'].dt.strftime('%d/%m/%Y')
            stock_data['close'] = stock_data['close'].apply(lambda x: str(x).replace('.', ','))

            return stock_data