import os
import time
from datetime import datetime
import pytz

def convert_date(text, date_type='%Y-%m-%d'):
    return datetime.strptime(text, date_type)

def convert_text_dateformat(text, origin_type = '%Y-%m-%d', new_type = '%Y-%m-%d'):
    return convert_date(text, origin_type).strftime(new_type)

def time_to_date(timestamp, date_format='%Y-%m-%d %H:%M:%S'):
    d = pytz.timezone('Asia/Ho_Chi_Minh').localize(datetime.fromtimestamp(timestamp))
    return d.strftime(date_format)


def date_to_time(date, date_format='%Y-%m-%d %H:%M:%S'):
    return int(time.mktime(datetime.strptime(date, date_format).timetuple()))


def str_to_int(text):
    text = str(text).replace(',', '')
    try:
        return int(text, base=10)
    except:
        return 0


def append_to_file(content, filename):
    with open(filename, 'a') as m_file:
        m_file.write(content + "\n")


def read_end_of_file(filename):
    if not os.path.exists(filename):
        return ''
    with open(filename, 'r') as f:
        lines = f.read().splitlines()
        lines.reverse()
        for line in lines:
            line = line.strip()
            if line:
                return line
        return ''
