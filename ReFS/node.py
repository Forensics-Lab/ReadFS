from typing import Union
from ReFS.dataArea import IndexEntries
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

    def indexRoot(self) -> IndexRootElement:
        size = self.formater.toDecimal(self.byteArray[0x50:0x50+0x4])
        indexRootType = self.formater.toDecimal(self.byteArray[size+0x50+0xD:size+0x50+0xE])
        return IndexRootElement(self.byteArray[0x50:0x50 + size], indexType=indexRootType)

    def indexHeader(self) -> IndexHeader:
        return IndexHeader(self.byteArray[self.indexHeaderOffset:self.indexHeaderOffset + 0x28])

    def dataArea(self) -> IndexEntries:
        # this function will need refoctoring.
        # the plan is to find a cleaner way to get the key:value pairs from the data area within the Container Table.
        indexHeader = self.indexHeader()
        keysStartOffset = indexHeader.keyIndexStart() + self.indexHeaderOffset
        keysEndOffset = indexHeader.keyIndexEnd() + self.indexHeaderOffset
        keysNumber = indexHeader.keyIndexEntries()
        keysBlock = self.byteArray[keysStartOffset:keysEndOffset]
        return IndexEntries(self.byteArray, keysBlock, keysNumber, self.indexHeaderOffset)

    def info(self) -> str:
        return f"{self.pageheader.info()}\n"\
               f"{self.indexRoot().info()}\n"\
               f"{self.indexHeader().info()}"
