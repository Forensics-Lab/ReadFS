from typing import Union
from ReFS.pageHeader import PageHeader
from ReFS.indexHeader import IndexHeader
from bytesFormater.formater import Formater
from ReFS.pageDescriptor import PageDescriptor
from ReFS.indexRootElement import IndexRootElement


class Node:
    def __init__(self, byteArray:Union[list[bytes], tuple[bytes], set[bytes]]) -> None:
        self.byteArray = byteArray
        self.formater = Formater()
        self.pageheader = PageHeader(self.byteArray[0x0:0x50])

    def indexRoot(self):
        size = IndexRootElement(self.byteArray[0x50:0x50+0x4]).size()
        return IndexRootElement(self.byteArray[0x50:0x50 + size])
    
    def indexHeader(self):
        offset = self.indexRoot().size() + 0x50
        return IndexHeader(self.byteArray[offset:offset + 0x28])

    def info(self):
        return f"{self.pageheader.info()}\n"\
               f"{self.indexRoot().info()}\n"\
               f"{self.indexHeader().info()}\n"