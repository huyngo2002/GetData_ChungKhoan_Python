import os, datetime
import time
from core.excel import Excel
from core.utilities import *
from DataLoader import DataLoader

finishFlag = False

def clear():
    os.system('clear')

def signal_handler(signal, frame):
    global finishFlag
    finishFlag = True
    print('You pressed Ctrl+C!')

def get_data():
    excel_path = str(args.excel)

    if ';' in args.symbol:
        symbols = str(args.symbol).strip().split(';')
    else:
        symbols = [str(args.symbol).strip()]

    symbols = [x.upper() for x in symbols]

    time_delay = str_to_int(args.delay)

    start_date = str(args.start_date).strip()
    end_date = str(args.end_date).strip()

    if start_date == 'None' or end_date == 'None':
        start_date = ''
        end_date = ''

    excel = Excel(symbols, excel_path)

    for stock in symbols:
        if finishFlag:
            break
        loader = DataLoader(stock, start_date, end_date)
        data = loader.download()

        excel.active_sheet(stock)
        last_date = excel.last_date(stock)
        last_time = None
        check_first_cell = False

        if last_date:
            last_time = date_to_time(last_date, date_format='%Y-%m-%d')

        for index, row in data.iterrows():
            if finishFlag:
                break
            high = row['close']
            volume = row['volume']
            date = index.strftime('%Y-%m-%d')
            check_date = True

            if not check_first_cell and excel.is_update(stock, high, volume, date):
                print('Clear.....')
                excel.clear_all(stock)
                excel.add_data(stock, high, volume, date)
                check_date = False
                last_date = False 

            check_first_cell = True
            if last_date and check_date:
                current_time = date_to_time(date, date_format='%Y-%m-%d')
                if current_time <= last_time:
                    continue
                last_date = None
            
            excel.add_data(stock, high, volume, date)
        
        if time_delay:
            time.sleep(time_delay)
    
    excel.save()
    clear()

def start():
    time_load_data = '00:30:00'
    next_date_check = time_to_date(time.time(), date_format='%Y-%m-%d')
    next_date_check = next_date_check + ' ' + time_load_data
    timeout = date_to_time(next_date_check) - time.time()

    while True:
        if finishFlag:
            break
        
        if timeout <= 0:
            if finishFlag:
                break
            get_data()
            next_date_check = time_to_date(time.time() + 86400, date_format='%Y-%m-%d')
            next_date_check = next_date_check + ' ' + time_load_data
            timeout = date_to_time(next_date_check) - time.time()

        print('Next load data {date} - Timeout: {seconds} seconds'.format(date=next_date_check, seconds=timeout))
        time.sleep(timeout)
        timeout = -1

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser('Tool realtime data & data')

    parser.add_argument('--excel', metavar='string', required=True, help='File excel')
    parser.add_argument('--symbol', metavar='string', required=True,
                        help='Ma chung khoan, vd: VIC;AAA;ABC;XYZ')
    parser.add_argument('--start_date', metavar='string', required=False,
                        help='Ngay bat dau, vd: 2017-08-10')
    parser.add_argument('--end_date', metavar='string', required=False,
                        help='Ngay ket thuc, vd: 2017-08-15')
    parser.add_argument('--delay', metavar='int', required=False,
                        help='Thoi gian delay (giay) giua cac lan lay du lieu, vd: 10')
    args = parser.parse_args()
    
    start()


    
