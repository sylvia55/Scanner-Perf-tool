import abc


class ReadData(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def read_content(self, input):
        """read file content or eml content"""
        return

    @abc.abstractmethod
    def read_content_from_folder(self):
        """read file in folder"""
        return

    @abc.abstractmethod
    def serialize_2_string(self, DataCollection, block, stritem):
        """convert protobuf to string"""
        return