

def PromtForDataCollection(transport, blockunit, stritem):

    block_item = transport.blockItemList.add()
    block_item.partType = blockunit.partType
    block_item.blockDescription = blockunit.blockDescription
    block_item.content = blockunit.content
    block_item.action = blockunit.action

    transport.strItemList.append(stritem)
