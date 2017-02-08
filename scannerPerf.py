import readMessage
import WriteResult
import xlsxwriter
import readFile
import threading
import ConfigParser
import os


def read_config(param):
    config = ConfigParser.ConfigParser()
    config.read('bin/App.config')
    param = config.get('Scanner', param)
    return param


def for_file():

    fileproto = readFile.ReadFile('./sample')
    return fileproto


def for_eml():

    r = readMessage.ReadMessage('sample/eml')
    return r


def multiple_thread_common(fileoreml):

    workbook = xlsxwriter.Workbook('result/demo-'+str(os.getpid())+'.xlsx')
    worksheet = workbook.add_worksheet()
    w = WriteResult.WriteResult(worksheet)
    a, z = fileoreml.prepare_post_data()
    thread_all = []
    for i in range(int(read_config('thread_number'))):
        t = threading.Thread(target=fileoreml.post_2scanner, args=(a, z))
        thread_all.append(t)
        t.start()
    for t in thread_all:
        t.join()
    results = fileoreml.get_results()
    for each in results:
        w.write_excel(each)
    workbook.close()


def main():
    if int(read_config('file_or_eml')) == 1:
        target = for_file()

    else:
        target = for_eml()
    repeat_times = int(read_config('repeat_time'))
    for i in range(repeat_times):
        multiple_thread_common(target)

if __name__ == '__main__':
    main()
