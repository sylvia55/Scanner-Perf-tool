import messageInterface_pb2


class AtlasProtobufEntity():


    def __init__(self, partType='attachment', blockDescription='mailbody', content='', action=''):
        self.blockunit = messageInterface_pb2.BlockUnit()
        self.partType = partType
        self.blockDescription = blockDescription
        self.content = content
        self.action = action

    def setPartType(self, value):
        self.blockunit.partType = value

    def getPartType(self):
        return self.blockunit.partType

    def setBlockDescription(self, value):
        self.blockunit.blockDescription = value

    def getBlockDescription(self):
        return self.blockunit.blockDescription

    def setContent(self, value):
        self.blockunit.content = value

    def getContent(self):
        return self.content

    def setAction(self, value):
        self.blockunit.action = value

    def getAction(self):
        return self.blockunit.action

    def getBlockUnit(self):
        return self.blockunit

def PromtForDataCollection(transport, blockunit, stritem):

    block_item = transport.blockItemList.add()
    block_item.partType = blockunit.partType
    block_item.blockDescription = blockunit.blockDescription
    block_item.content = blockunit.content
    block_item.action = blockunit.action

    transport.strItemList.append(stritem)