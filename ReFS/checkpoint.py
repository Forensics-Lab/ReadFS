from ReFS.node import Node
from bytesReader.reader import Reader
from ReFS.page import PageHeader, PageDescriptor

class Checkpoint(Reader):
    def __init__(self, filePath:str, readByteRange:list, offset=0) -> None:
        super().__init__(filePath)
        self.byteArray = super().getBytes(readByteRange, offset=offset)
        self.pageHeader = PageHeader(self.byteArray[0x0:0x50])
        self.pageDescriptor = PageDescriptor(self.byteArray[self.selfDescriptorOffset():][:self.selfDescriptorLength()])
        self.__pointerList = self.pointerList()

    def __getVirtualClusterAddress(self, byteNumber:int) -> int:
        return self.formater.toDecimal(self.byteArray[byteNumber:byteNumber+104][:4])

    def __phisycalClustersAddress(self, virtualAddresses: list) -> list:
        plist = []
        for index, address in enumerate(virtualAddresses):
            if index not in (7, 8, 12): # Skipping Container Table, Container Table Duplicate and Small Allocator Table
                address = int(hex(address)[3:], 16)
            plist.append(address * len(self.byteArray))
        return plist

    def majorVersion(self) -> int:
        return self.formater.toDecimal(self.byteArray[0x54:0x56])

    def minorVersion(self) -> int:
        return self.formater.toDecimal(self.byteArray[0x56:0x58])

    def selfDescriptorOffset(self) -> int:
        return self.formater.toDecimal(self.byteArray[0x58:0x5C])

    def selfDescriptorLength(self) -> int:
        return self.formater.toDecimal(self.byteArray[0x5C:0x60])

    def chkpVirtualClock(self) -> int:
        return self.formater.toDecimal(self.byteArray[0x60:0x68])

    def allocatorVirtualClock(self) -> int:
        return self.formater.toDecimal(self.byteArray[0x68:0x70])

    def oldestLogRecordReference(self) -> int:
        return self.formater.toDecimal(self.byteArray[0x78:0x7C])

    def alignment(self) -> int:
        return self.formater.toDecimal(self.byteArray[0x7C:0x80])

    def reserved(self) -> int:
        return self.formater.toDecimal(self.byteArray[0x80:0x88])

    def pointerCount(self) -> int:
        return self.formater.toDecimal(self.byteArray[0x90:0x94])

    def pointerList(self) -> list:
        plist = self.byteArray[0x94:0xC8]
        return self.__phisycalClustersAddress([self.__getVirtualClusterAddress(self.formater.toDecimal(plist[i:i+4])) for i in range(0, len(plist), 4)])

    def objectIDPointer(self) -> int:
        return self.__pointerList[0]

    def mediumAllocatorPointer(self) -> int:
        return self.__pointerList[1]

    def containerAllocatorPointer(self) -> int:
        return self.__pointerList[2]

    def schemaTablePointer(self) -> int:
        return self.__pointerList[3]

    def parentChildTablePointer(self) -> int:
        return self.__pointerList[4]

    def objectIDDuplicatePointer(self) -> int:
        return self.__pointerList[5]

    def blockReferenceCountPointer(self) -> int:
        return self.__pointerList[6]

    def containerTablePointer(self) -> int:
        return self.__pointerList[7]

    def containerTableDuplicatePointer(self) -> int:
        return self.__pointerList[8]

    def schemaTableDuplicatePointer(self) -> int:
        return self.__pointerList[9]

    def containerIndexTablePointer(self) -> int:
        return self.__pointerList[10]

    def integrityStateTablePointer(self) -> int:
        return self.__pointerList[11]

    def smallAllocatorTablePointer(self) -> int:
        return self.__pointerList[12]

    def info(self) -> str:
        return f"{self.pageHeader.info()}\n"\
               f"<<======================[Checkpoint]=====================>>\n"\
               f"[+] ReFS Version: {self.majorVersion()}.{self.minorVersion()}\n"\
               f"[+] Self Descriptor Relative Offset: {self.selfDescriptorOffset()}\n"\
               f"[+] Self Descriptor Length: {self.selfDescriptorLength()}\n"\
               f"[+] Checkpoint Virtual Clock: {self.chkpVirtualClock()}\n"\
               f"[+] Allocator Virtual Clock: {self.allocatorVirtualClock()}\n"\
               f"[+] Oldest Log Record: {self.oldestLogRecordReference()}\n"\
               f"<<=============[Pointers Bytes Offset Info]==============>>\n"\
               f"[+] Object ID Table: {self.objectIDPointer()}\n"\
               f"[+] Duplicate Object ID Table: {self.objectIDDuplicatePointer()}\n"\
               f"[+] Medium Allocator Table: {self.mediumAllocatorPointer()}\n"\
               f"[+] Container Allocator Table: {self.containerAllocatorPointer()}\n"\
               f"[+] Schema Table: {self.schemaTablePointer()}\n"\
               f"[+] Duplicate Schema Table: {self.schemaTableDuplicatePointer()}\n"\
               f"[+] Parent Child Table: {self.parentChildTablePointer()}\n"\
               f"[+] Block Reference Count Table: {self.blockReferenceCountPointer()}\n"\
               f"[+] Container Table: {self.containerTablePointer() * len(self.byteArray)}\n"\
               f"[+] Duplicate Container Table: {self.containerTableDuplicatePointer() * len(self.byteArray)}\n"\
               f"[+] Container Index Table: {self.containerIndexTablePointer()}\n"\
               f"[+] Integrity State Table: {self.integrityStateTablePointer()}\n"\
               f"[+] Small Allocator Table: {self.smallAllocatorTablePointer() * len(self.byteArray)}\n"\
               f"{self.pageDescriptor.info()}"
