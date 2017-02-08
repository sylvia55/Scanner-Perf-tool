import requests
from urllib import quote
from os import listdir
from os.path import isfile, join
import scannerPerf

class WriteResult(object):

    count = 0

    def __init__(self, worksheet):
        self.worksheet = worksheet

    def write_excel(self, result):

        self.write_result(self.worksheet, result)
        # workbook.close()

    def write_result(self, worksheet, result):

        row = 0
        col = 0

        for l in result:
            worksheet.write(row+self.count, col, l)
            col += 1
            # worksheet.write('B'+self.count, )
        print self.count
        self.count += 1


def post_req(data, header):
    # print dir(scannerPerf)
    url = scannerPerf.read_config('url')
    url = 'http://' + url +':8080/scan'
    session = requests.Session()
    session.trust_env = False
    request = session.post(url, data=data, headers=header)
    return request


#def postreq(data, header, url):
#    request = requests.post(url, data=data, headers=header)
#    return request


def load_header(file):
    # header = {}
    try:
        with open(file, 'rb') as f:
            d = {}
            while True:
                line = f.readline()
                if not line: break
                array = line.split(':', 1)
                # print array
                array[1] = quote(array[1].strip(), safe='')
                d[array[0].strip()] = array[1]

            return d

    except Exception, e:
        print e


def load_policy():

    # policies = [loadHeader(join('.\policy', f)) for f in listdir('.\policy') if isfile(join('.\policy', f))]
    policy = {f: load_header(join('.\policy', f)) for f in listdir('.\policy') if isfile(join('.\policy', f))}
    return policy
