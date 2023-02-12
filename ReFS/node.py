from ReFS.page import *
from bytesReader.reader import Reader
from ReFS.dataArea import IndexEntries
from ReFS.indexHeader import IndexHeader
from ReFS.indexRootElement import IndexRootElement


class Node(Reader):
    def __init__(self, filePath:str, readByteRange:list, offset=0) -> None:
        super().__init__(filePath)
        self.byteArray = super().getBytes(readByteRange, offset=offset)
        self.pageHeader = PageHeader(self.byteArray[0x0:0x50])
        self.indexHeaderOffset = self.indexRoot().size() + 0x50

    def indexRoot(self) -> IndexRootElement:
        size = self.formater.toDecimal(self.byteArray[0x50:0x50+0x4])
        indexType = self.formater.toDecimal(self.byteArray[size+0x50+0xD:size+0x50+0xE])
        return IndexRootElement(self.byteArray[0x50:0x50 + size], indexType=indexType)

    def indexHeader(self) -> IndexHeader:
        return IndexHeader(self.byteArray[self.indexHeaderOffset:self.indexHeaderOffset + 0x28])

    def dataArea(self) -> IndexEntries:
        # this function will need refactoring.
        # the plan is to find a cleaner way to get the key:value pairs from the data area within the Container Table.
        indexHeader = self.indexHeader()
        keysStartOffset = indexHeader.keyIndexStart() + self.indexHeaderOffset
        keysEndOffset = indexHeader.keyIndexEnd() + self.indexHeaderOffset
        keysNumber = indexHeader.keyIndexEntries()
        keysBlock = self.byteArray[keysStartOffset:keysEndOffset]
        return IndexEntries(self.byteArray, keysBlock, keysNumber, self.indexHeaderOffset)

    def info(self) -> str:
        return f"{self.pageHeader.info()}\n"\
               f"{self.indexRoot().info()}\n"\
               f"{self.indexHeader().info()}"
