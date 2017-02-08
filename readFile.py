import messageInterface_pb2
import logging
import AtlasProto
import datetime, time
import postReq
from os import listdir
from os.path import isfile, join
import threading
from ReadData import ReadData


class ReadFile(ReadData):

    all_results = []
    def __init__(self, folder):
        self.folder = folder

    def read_content(self, filename):
        try:
            with open(filename, 'rb') as f:
                return f.read()
        except Exception, e:
            print e

    def read_content_from_folder(self):

        files_in_folder = [f for f in listdir(self.folder) if isfile(join(self.folder, f))]
        filecontents = []
        for f in files_in_folder:
            tmp = {}
            tmp[f] = self.read_content(join(self.folder, f))
            filecontents.append(tmp)
        return filecontents

    def serialize_2_string(self, DataCollection, block, stritem):
        logging.debug(type(block))
        AtlasProto.PromtForDataCollection(DataCollection.units.add(), block, stritem)
        string = DataCollection.SerializeToString()
        return string

    def generate_block_for_file(self, content):   ## need to modify

        blocks = []
        for f in content:
            # block = []
            for (k, v) in f.items():
                blocks.append(AtlasProto.AtlasProtobufEntity('attachment', k, v, 2))
            #     print 'k is : ' + k
            #     print 'v is : ' + v
            # print len(blocks)
        return blocks

    def prepare_post_data(self):
        content = self.read_content_from_folder()
        # print type(content)
        # print content

        strArray = ['1']*len(content)

        blocks = self.generate_block_for_file(content)

        return blocks, strArray

    def post_2scanner(self, blocks, strArray):

        headers = postReq.load_policy()
        for block, str in zip(blocks, strArray):

            DataCollection = messageInterface_pb2.DataCollection()
            storestring = self.serialize_2_string(DataCollection, block, str)
            # print storestring
            for (k, v) in headers.items():
                results = []
                a = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
                start_time = time.time()
                res = postReq.post_req(storestring, v)
                end_time = (time.time()-start_time)*1000
                b = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
                results.append(block.blockDescription)
                results.append(k)
                results.append(a)
                results.append(b)
                results.append(end_time)
                if 'X-ATLAS-SCAN-FILTER' in res.headers.keys() and res.headers['X-ATLAS-SCAN-ACTION'] != '0':
                    results.append(res.headers['X-ATLAS-SCAN-FILTER'])
                else:
                    results.append('0')
                results.append(res.headers['X-ATLAS-SCAN-ACTION'])
                results.append(res.status_code)
                logging.debug(res.text)
                logging.debug(threading.current_thread())
                self.all_results.append(results)
        # return self.all_results

    def get_results(self):

        return self.all_results
        # workbook.close()
                # results.append(res)

    # def multi_thread_file(self):
    #
    #     workbook = xlsxwriter.Workbook('demo.xlsx')
    #     worksheet = workbook.add_worksheet()
    #     w = WriteResult.WriteResult(worksheet)
    #     a, z = self.prepare_post_data()
    #     # while i < threadNumber:
    #     t1 = threading.Thread(target=self.post_file2scanner, args=(a, z))
    #     t2 = threading.Thread(target=self.post_file2scanner, args=(a, z))
    #     t1.start()
    #     t2.start()
    #     t1.join()
    #     t2.join()
    #     results = self.get_results()
    #     for each in results:
    #         w.write_excel(each)
    #     workbook.close()

# def main():
#     fileProto = ReadFile('.\sample')
#     # fileProto.post_file2scanner()
#     fileProto.multi_thread_file()
#
#
#
# if __name__ == "__main__":
#     main()
