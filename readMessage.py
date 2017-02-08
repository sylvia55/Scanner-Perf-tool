import email
from os import listdir
from os.path import isfile, join
import messageInterface_pb2
import logging
import time
import AtlasProto
import postReq
import datetime
import threading
from ReadData import ReadData


class ReadMessage(ReadData):
    """Summary of class ReadMessage here,
    It's used to read eml in eml folder, and generate eml to Protobuf format
    Attributes:
        folder: folder contains eml sample files
    @Author Sylvia
    """
    all_results = []
    def __init__(self, folder):
        self.folder = folder

    def read_content(self, filename):
        """read single eml file
        parse attachment and mailbody from eml file,
        return dict contains attachment name and attachment content, mail_body and mail body content
        """
        eml = []
        msg = email.message_from_file(open(join(self.folder, filename), 'r'))
        
        # get mail property
        mail_property = {}
        if "from" in msg:
            mail_property["from"] = msg["from"]
        if "to" in msg:
            mail_property["to"] = msg["to"]
        if "cc" in msg:
            mail_property["cc"] = msg["cc"]
        if "subject" in msg:
            mail_property["subject"] = msg["subject"]
        
        # get mail body and attachment content
        for par in msg.walk():
            if not par.is_multipart():
                name = par.get_param("name")
                if name:
                    h = email.Header.Header(name)
                    dh = email.Header.decode_header(h)
                    fname = dh[0][0]
                    # print 'attachmentname: ', fname
                    data = par.get_payload(decode=True)

                else:
                    fname = 'mail_body'
                    data = par.get_payload(decode=True)
                # eml[fname] = data
                eml.append({fname:data})
        return [mail_property, eml]

    def read_content_from_folder(self):
        """read all eml file from target folder
        
        """
        emls = [e for e in listdir(self.folder) if isfile(join(self.folder, e))]
        logging.debug(len(emls))
        logging.debug(emls)
        eml_result = []

        for e in emls:
            tmp = {}
            logging.debug(e)
            tmp[e] = self.read_content(e)
            eml_result.append(tmp)
            logging.debug(eml_result)
        logging.debug(len(eml_result))
        logging.debug(eml_result)
        return eml_result

    def generate_block_for_message(self, content):
        logging.debug(content)
        blocks = {}
        for e in content:# each file
            block = []
            for (ek, ev) in e.items():    #email subject, filename
                if (len(e[ek]) >= 2):
                    for attachment in e[ek][1]:
                        for (k, v) in attachment.items():
                            logging.debug(v)
                            if k == 'mail_body':
                                parttype = 'body'
                            else:
                                parttype = 'attachment'
                                logging.debug(v)
                            block.append(AtlasProto.AtlasProtobufEntity(parttype, k, v, 2))  # need to modify, put filename
            blocks[ek] = block
        logging.debug(blocks)
        # print blocks
        return blocks

    def serialize_2_string(self, DataCollection, block, strItem):
        units = DataCollection.units.add()
        if "from" in strItem:
            units.strItemList.append("FROM:" + strItem["from"])
        if "to" in strItem:
            units.strItemList.append("TO:" + strItem["to"])
        if "cc" in strItem:
            units.strItemList.append("CC:" + strItem["cc"])
        if "subject" in strItem:
            units.strItemList.append("SUBJECT:" + strItem["subject"])
        logging.debug(type(block))
        logging.debug(block)
        for (b, s) in zip(block, strItem):
            logging.debug(b)
            logging.debug(s)
            AtlasProto.PromtForDataCollection(units, b, s)
        # new.PromtForDataCollection(DataCollection.units.add(), block, stritem)
        string = DataCollection.SerializeToString()
        # print string
        return string

    def get_results(self):
        return self.all_results

    def prepare_post_data(self):

        blocks = self.read_content_from_folder()
        logging.debug(len(blocks))
        # rm.generate_block_for_message(blocks)

        a = self.generate_block_for_message(blocks)
        strArray = []
        for i in range(len(blocks)):
            strArray.append('hello, item'+str(i))

        return a, strArray
        # strItem = self.generate_str_item_for_message(blocks)

        # return a, strItem

    def generate_str_item_for_message(self, content):
        logging.debug(content)
        strItem = {}
        for e in content:    # each file
            for (ek, ev) in e.items():    #email subject, filename
                if (len(ev) >= 1):
                    strItem[ek] = ev[0]
                else:
                    strItem[ek] = {}
        logging.debug(strItem)
        return strItem

    def post_2scanner(self, a, strItem):

        headers = postReq.load_policy()
        # url = 'http://localhost:8080/scan'
        for block, str in zip(a.values(), strItem):
            DataCollection = messageInterface_pb2.DataCollection()
            storestring = self.serialize_2_string(DataCollection, block, str)
            logging.debug(storestring)
            for (k,v) in headers.items():
                results = []
                before_time = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
                start_time = time.time()
                res = postReq.post_req(storestring, v)
                cost_time = (time.time()-start_time)*1000
                after_time = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
                results.append(a.keys()[a.values().index(block)])
                results.append(k)
                results.append(before_time)
                results.append(after_time)
                results.append(cost_time)
                if 'X-ATLAS-SCAN-FILTER' in res.headers.keys() and res.headers['X-ATLAS-SCAN-ACTION'] != '0':
                    results.append(res.headers['X-ATLAS-SCAN-FILTER'])
                else:
                    results.append('0')
                results.append(res.headers['X-ATLAS-SCAN-ACTION'])
                results.append(res.status_code)
                if (cost_time > 100):
                    results.append('abnormal')
                logging.debug(threading.current_thread())
                logging.debug(res.text)
                self.all_results.append(results)
    
    # def post_2_scanner_thread(self, blocks, strArray):
    #     count = 100
    #     while (count > 0):
    #         self.post_2scanner(blocks, strArray)
    #         count = count - 1
    #
    #     logging.debug("thread end")

def main():
    r = ReadMessage('sample\\eml')
    r.post_2scanner()


if __name__ == '__main__':
    main()

