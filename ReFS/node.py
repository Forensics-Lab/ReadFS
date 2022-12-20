from typing import Union
from ReFS.dataArea import DataArea
from ReFS.pageHeader import PageHeader
from ReFS.indexHeader import IndexHeader
from bytesFormater.formater import Formater
from ReFS.indexRootElement import IndexRootElement

class Node:
    def __init__(self, byteArray:Union[list[bytes], tuple[bytes], set[bytes]]) -> None:
        self.byteArray = byteArray
        self.formater = Formater()
        self.pageheader = PageHeader(self.byteArray[0x0:0x50])
        self.indexHeaderOffset = self.indexRoot().size() + 0x50

    def indexRoot(self):
        size = self.formater.toDecimal(self.byteArray[0x50:0x50+0x4])
        indexRootType = self.formater.toDecimal(self.byteArray[size+0x50+0xD:size+0x50+0xE])
        return IndexRootElement(self.byteArray[0x50:0x50 + size], indexType=indexRootType)

    def indexHeader(self):
        return IndexHeader(self.byteArray[self.indexHeaderOffset:self.indexHeaderOffset + 0x28])

    def dataArea(self):
        indexHeader = self.indexHeader()
        keysStartOffset = indexHeader.keyIndexStart() + self.indexHeaderOffset
        keysEndOffset = indexHeader.keyIndexEnd() + self.indexHeaderOffset
        keysNumber = indexHeader.keyIndexEntries()
        keysBlock = self.byteArray[keysStartOffset:keysEndOffset]
        keys = []
        for i in range(0, keysNumber, 4):
            keyOffset = (self.formater.toDecimal(keysBlock[i:i+4]) & 0x0000ffff) + self.indexHeaderOffset
            keySize = self.formater.toDecimal(self.byteArray[keyOffset:keyOffset+0x4])
            keys.append(DataArea(self.byteArray[keyOffset:keyOffset + keySize]))
        return tuple(keys)

    def info(self):
        return f"{self.pageheader.info()}\n"\
               f"{self.indexRoot().info()}\n"\
               f"{self.indexHeader().info()}"\
