import xlrd
import csv
import ConfigParser
import datetime
import  time
from ScanUnit import read_config


def read_xlsx():
    workbook = xlrd.open_workbook('test\scanresult_2644.csv')
    worksheet = workbook.sheet_by_name('Sheet1')
    num_rows = worksheet.nrows
    curr_row = 0
    result_not_dda_mal = []
    result_dda_mal = []
    for col in range(num_rows):
        value = worksheet.cell(col, 2)
        value_int = int(value.value)
        if value_int == 8 or value_int == 5:
            result_dda_mal.append({str(worksheet.cell(col,0).value):value_int})
        else:

            result_not_dda_mal.append({str(worksheet.cell(col,0).value):value_int})
    print result_not_dda_mal
    print result_dda_mal



def read_csv():
    result_dda = []
    result_empty_not_dda = []
    with open('test\scanresult_3368.csv', 'rb') as f:
        reader = csv.reader(f)
        reader.next()
        # for row in reader:
        #     print type(row[6])
        for row in reader:
            print row[6]
            if row[6].strip():
                # print type(row[6])
                # print int(row[6])
                if int(row[6].strip()) == 1 or int(row[6].strip()) == 2:
                    result_dda.append({row[0]:row[6]})
                    # print a[0]
            else:
                result_empty_not_dda.append({row[0]:row[6]})
    return result_dda, result_empty_not_dda

# (dda, not_dda) = read_csv()



def write_file(string):
    try:
        with open('not_dda.txt', 'wb') as f:
            f.write(string)
                # count += 1
    except Exception, e:
        print e


# print len(dda)
# print len(not_dda)
# print not_dda


class hello_sylvia():
    def __init__(self, number):
        self.number = number

    def test(self):
        self.hello = 'nihao'
        self.number = 8

    def get_test(self):
        return self.hello

    def change_test(self):
        self.hello = 'changed by func'

    def get_number(self):
        return self.number

# t = test(1)
# t.test()
# print t.get_test()
# t.change_test()
# print t.get_test()



def hello_config():

    config = ConfigParser.ConfigParser()
    config.read('unit\config.ini')
    print config.sections()

# hello_config()

print datetime.timedelta(days=1)
print datetime.datetime.now()
print datetime.datetime.now() - datetime.timedelta(days=30)

def main():
    # tag = read_config('cases', 'category')
    # print tag
    # print type(tag)
    config = ConfigParser.ConfigParser()
    config.read('unit\config.ini')
    for section in config.sections():
        if section != 'cases':
            print 'true'
        else:
            print 'false'


if __name__ == '__main__':
    main()