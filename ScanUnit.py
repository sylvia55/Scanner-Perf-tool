import ConfigParser
import readFile
import readMessage
from os.path import isfile, join
import postReq
import messageInterface_pb2
from constants import action, filter
import xlsxwriter
import WriteResult
import logging
import os

logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] %(filename)s[line:%(lineno)d] %(levelname)s: %(message)s',
    datefmt = '%a, %d %b %Y %H:%M:%S',
    filename = 'case.log',
    filemode = 'a')

def read_config(category, param):
    config = ConfigParser.ConfigParser()
    config.read('unit\config.ini')
    param = config.get(category, param)
    return param


def test_config():

    config = ConfigParser.ConfigParser()
    config.read('unit\config.ini')
    tag = config.get('cases', 'category')
    # if tag == 'all':
    #     return config.sections()
    print tag
    print 'this is '
    print config.sections()
    a = []
    for section in config.sections():
        if tag == 'all':
            if section != 'cases':
                a.append(section)
        else:
            try:
                if str(config.get(section, 'tag')) == tag:
                    a.append(section)
                    print config.get(section, 'tag')
                else:
                    print 'else here'
            except Exception, e:
                print e
    return a


def for_file(path):

    fileproto = readFile.ReadFile(path)
    return fileproto


def for_eml(path):

    r = readMessage.ReadMessage(path)
    return r


def post_file_2scanner(target, blocks, strArray, policy):
    # all_results = []
    print 'inside post_file_2scanner'
    for block, str in zip(blocks, strArray):
        results = {}
        DataCollection = messageInterface_pb2.DataCollection()
        storestring = target.serialize_2_string(DataCollection, block, str)
        logging.debug(storestring)

        res = postReq.post_req(storestring, policy)
        print 'result in response'
        print res.headers
        if res.status_code == 200:
            print 'status_code 200'
            # results['X-STATUS-CODE'] = 200
        # results.append(block.blockDescription)
            results['X-ATLAS-SCAN-ACTION'] = res.headers['X-ATLAS-SCAN-ACTION']
            # results['X-ATLAS-SCAN-FILTER'] = res.headers['X-ATLAS-SCAN-FILTER']
            if 'X-ATLAS-SCAN-FILTER' in res.headers.keys() and res.headers['X-ATLAS-SCAN-ACTION'] != '0':
                results['X-ATLAS-SCAN-FILTER'] = res.headers['X-ATLAS-SCAN-FILTER']
            else:
                results['X-ATLAS-SCAN-FILTER'] = '0'
        else:
             results['X-ATLAS-SCAN-ACTION'] = 'failed'
             results['X-ATLAS-SCAN-FILTER'] = 'failed'
        results['X-STATUS-CODE'] = res.status_code
# all_results.append(results)
    return results


def post_eml_2scanner(target, blocks, strArray, policy):
    # all_results = {}
    for block, str in zip(blocks.values(), strArray):
        DataCollection = messageInterface_pb2.DataCollection()
        storestring = target.serialize_2_string(DataCollection, block, str)
        results = {}
        res = postReq.post_req(storestring, policy)
        # results.append(blocks.keys()[blocks.values().index(block)])
        if res.status_code == 200:
            print 'status_code 200'
            results['X-ATLAS-SCAN-ACTION'] = res.headers['X-ATLAS-SCAN-ACTION']
            # results['X-ATLAS-SCAN-FILTER'] = res.headers['X-ATLAS-SCAN-FILTER']
            if 'X-ATLAS-SCAN-FILTER' in res.headers.keys() and res.headers['X-ATLAS-SCAN-ACTION'] != '0':
                results['X-ATLAS-SCAN-FILTER'] = res.headers['X-ATLAS-SCAN-FILTER']
            else:
                results['X-ATLAS-SCAN-FILTER'] = '0'
        else:
             results['X-ATLAS-SCAN-ACTION'] = 'failed'
             results['X-ATLAS-SCAN-FILTER'] = 'failed'
        results['X-STATUS-CODE'] = res.status_code
        # all_results.append(results)
    logging.debug(results)
    return results


def validation_result(casename, results):

    logging.debug(results)
    scan_result = []
    if results['X-ATLAS-SCAN-ACTION'] == read_config(casename, 'case_action') and results['X-ATLAS-SCAN-FILTER'] == read_config(casename, 'case_filter'):
        print type(results['X-ATLAS-SCAN-ACTION'])
        print 'same as respect '+action[results['X-ATLAS-SCAN-ACTION']]
        case_result = 'success'
    else:
        print 'expection is '+ read_config(casename, 'case_action')
        print 'but real action is '+action[results['X-ATLAS-SCAN-ACTION']]
        case_result = 'fail'
    scan_result.append(casename)
    scan_result.append(case_result)
    scan_result.append(read_config(casename, 'case_action'))
    scan_result.append(action[results['X-ATLAS-SCAN-ACTION']])
    scan_result.append(read_config(casename, 'case_filter'))
    scan_result.append(filter[results['X-ATLAS-SCAN-FILTER']])
    scan_result.append(results['X-STATUS-CODE'])
    # scan_result.append()

    return scan_result


def test_case(casename, w):

    print 'begin test_case'
    path = join('unit', casename, 'sample')
    policy = postReq.load_header(join('unit', casename, read_config(casename, 'case_policy')))

    if read_config(casename, 'case_type') == 'sp':
        target = for_file(path)
        a, z = target.prepare_post_data()
        results = post_file_2scanner(target, a, z, policy)
    elif read_config(casename, 'case_type') == 'ex':
        target = for_eml(path)
        a, z = target.prepare_post_data()
        results = post_eml_2scanner(target, a, z, policy)
    else:
        print 'invalid case_type for: '+ casename
    #     results = ''
    print results
    print 'inside test case'
    scan_result = validation_result(casename, results)
    w.write_excel(scan_result)
    return scan_result

if __name__ == '__main__':
    workbook = xlsxwriter.Workbook('case_result-'+str(os.getpid())+'.xlsx')
    worksheet = workbook.add_worksheet()
    w = WriteResult.WriteResult(worksheet)
    # test_case('eml', w)
    # test_case('icrc', w)
    # case_names = read_config('cases','case_name')
    # print type(case_names)
    # print len(case_names)
    # for case_name in case_names.split(','):
    #     test_case(case_name, w)

    for case_name in test_config():
        test_case(case_name, w)

    # email_content = []
    # for case_name in case_names.split(','):
    #     print case_name
    #     print len(case_names.split(','))
    #     email_content.append(test_case(case_name, w))
    #     # print read_config(case_name, 'case_action')
    # # print case_names
    # # print email_content
    # email = sendEmail.sendEmail()
    # email.initial_send_mail("subject is sylvia", email_content)
    workbook.close()
    # main('hhhh')