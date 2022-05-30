from os import path
import xlwings

from core.utilities import time_to_date, date_to_time, str_to_int


class Excel:

    def __init__(self, symbols, file_path):
        self.__symbols = symbols
        self.__file_path = file_path
        self.__wp = None
        self.__counts = {}
        self.__init_data()

    def __open_or_create_file(self):
        if path.exists(self.__file_path):
            self.__wp = xlwings.Book(self.__file_path)
        else:
            self.__wp = xlwings.Book()

    def __init_data(self):
        self.__open_or_create_file()
        names = []
        for sheet in self.__wp.sheets:
            row = 5
            while True:
                date = sheet.range('A{0}'.format(row)).value
                if not date:
                    break
                row += 1
            self.__counts.update({sheet.name: row})
            names.append(sheet.name)

        for symbol in self.__symbols:
            if symbol not in names:
                self.__counts.update({symbol: 1})
                self.__wp.sheets.add(symbol)

    def is_update(self, symbol, h, v, date):
        if self.__counts[symbol] <= 5:
            return False
        sheet = self.__wp.sheets[symbol]
        c_date = sheet.range('A{0}'.format(5)).value
        c_date = time_to_date(date_to_time(str(c_date)), date_format='%Y-%m-%d')
        c_h = sheet.range('B{0}'.format(5)).value
        c_v = int(sheet.range('C{0}'.format(5)).value)

        return date != c_date or h != c_h or v != c_v

    def active_sheet(self, name):
        self.__wp.sheets[name].activate()

    def save(self):
        self.__wp.save()

    def last_date(self, symbol):
        sheet = self.__wp.sheets[symbol]
        if self.__counts[symbol] <= 5:
            return None
        date = sheet.range('A{0}'.format(self.__counts[symbol] - 1)).value
        return time_to_date(date_to_time(str(date)), date_format='%Y-%m-%d')

    def clear_all(self, symbol):
        sheet = self.__wp.sheets[symbol]

        row = 1
        while row <= self.__counts[symbol]:
            sheet.range('A{0}'.format(row)).value = ''
            sheet.range('B{0}'.format(row)).value = ''
            sheet.range('C{0}'.format(row)).value = ''
            row += 1

        self.__counts[symbol] = 5

    def add_data(self, symbol, h, v, date):
        # print(symbol, '[{0}]'.format(self.__counts[symbol]), date, h, v)
        sheet = self.__wp.sheets[symbol]
        sheet.range('A{0}'.format(self.__counts[symbol])).value = date
        sheet.range('A{0}'.format(self.__counts[symbol])).number_format = 'dd/mm/yyyy'
        sheet.range('B{0}'.format(self.__counts[symbol])).value = h
        sheet.range('C{0}'.format(self.__counts[symbol])).value = v
        self.__counts[symbol] += 1
