from ReFS.Page import PageHeader
from Managers.Bytes import Formater
from ReFS.Index import DataArea, IndexHeader, IndexEntries, IndexElement

class Node():
    def __init__(self, _bytes: bytes) -> None:
        self.byteArray = _bytes
        self.formater = Formater()
        self.pageHeader = PageHeader(self.byteArray[0x0:0x50])
        self.indexHeaderOffset = self.indexRoot().size() + 0x50

    def indexRoot(self) -> IndexElement:
        size = self.formater.toDecimal(self.byteArray[0x50:0x50+0x4])
        return IndexElement(self.byteArray[0x50:0x50 + size])

    def indexHeader(self) -> IndexHeader:
        return IndexHeader(self.byteArray[self.indexHeaderOffset:self.indexHeaderOffset + self.indexRoot().rootFixedSize()])

    def dataArea(self) -> DataArea:
        dataAreaStart = self.indexHeader().dataAreaOffsetStart() + self.indexHeaderOffset
        dataAreaEnd = self.indexHeader().dataAreaOffsetEnd() + self.indexHeaderOffset
        return DataArea(self.byteArray[dataAreaStart:dataAreaEnd])

    def indexEntries(self) -> IndexEntries:
        return IndexEntries(self.dataArea().byteArray, self.indexHeader().keyIndexEntries(), self.pageHeader.tableIdentifier(), self.indexRoot().variableComponent())

    def info(self) -> str:
        return f"{self.pageHeader.info()}\n"\
               f"{self.indexRoot().info()}\n"\
               f"{self.indexHeader().info()}"
