from ReFS.Page import *
from struct import unpack
from Managers.Bytes import Formater

class Checkpoint():
    def __init__(self, _bytes: bytes) -> None:
        self.__byteArray = _bytes
        self.formater = Formater()
        self.__containerTableNodeEntries = None
        self.chStruct = self.formater.removeEmptyEntries(unpack("<80s4p2h2iq2i8s4s4p16p14i", self.__byteArray[:0xC8]))

    def setContainerTableEntries(self, entries:list):
        self.__containerTableNodeEntries = entries

    def convertToLCN(self, VCN: int = None, skipTable: bool = False, useContainerTable: bool = True) -> int:
        if skipTable: return VCN * len(self.__byteArray)
        offset = int(hex(VCN)[3:], 16)
        if useContainerTable:
            containerOffset = int(hex(VCN)[2]) - 1
            offset = (int(hex(self.__containerTableNodeEntries[containerOffset]["Container"]["Container LCN"])[:-2], 16) + offset)
        return offset * len(self.__byteArray)

    def majorVersion(self) -> int:
        return self.chStruct[1]

    def minorVersion(self) -> int:
        return self.chStruct[2]

    def ReFSVersion(self) -> str:
        return f"{self.majorVersion()}.{self.minorVersion()}"

    def selfDescriptorOffset(self) -> int:
        return self.chStruct[3]

    def selfDescriptorLength(self) -> int:
        return self.chStruct[4]

    def chkpVirtualClock(self) -> int:
        return self.chStruct[5]

    def allocatorVirtualClock(self) -> int:
        return self.chStruct[6]

    def oldestLogRecordReference(self) -> int:
        return self.chStruct[7]

    def unknown(self) -> bytes:
        return self.chStruct[8]

    def reserved(self) -> int:
        return self.chStruct[9]

    def pointerCount(self) -> int:
        return self.chStruct[10]

    def pointersList(self) -> list:
        return [self.formater.toDecimal(self.__byteArray[i:i+104][:4]) for i in self.chStruct[-self.pointerCount():]]

    def objectIDPointer(self) -> int:
        return self.convertToLCN(self.pointersList()[0])

    def mediumAllocatorPointer(self) -> int:
        return self.convertToLCN(self.pointersList()[1])

    def containerAllocatorPointer(self) -> int:
        return self.convertToLCN(self.pointersList()[2], useContainerTable=True)

    def schemaTablePointer(self) -> int:
        return self.convertToLCN(self.pointersList()[3])

    def parentChildTablePointer(self) -> int:
        return self.convertToLCN(self.pointersList()[4])

    def objectIDDuplicatePointer(self) -> int:
        return self.convertToLCN(self.pointersList()[5])

    def blockReferenceCountPointer(self) -> int:
        return self.convertToLCN(self.pointersList()[6], useContainerTable=True)

    def containerTablePointer(self) -> int:
        return self.convertToLCN(self.pointersList()[7], skipTable=True)

    def containerTableDuplicatePointer(self) -> int:
        return self.convertToLCN(self.pointersList()[8], skipTable=True)

    def schemaTableDuplicatePointer(self) -> int:
        return self.convertToLCN(self.pointersList()[9])

    def containerIndexTablePointer(self) -> int:
        return self.convertToLCN(self.pointersList()[10])

    def integrityStateTablePointer(self) -> int:
        return self.convertToLCN(self.pointersList()[11], useContainerTable=True)

    def smallAllocatorTablePointer(self) -> int:
        return self.convertToLCN(self.pointersList()[12], skipTable=True)

    def info(self) -> str:
        return f"{PageHeader(self.chStruct[0]).info()}\n"\
               f"<<======================[Checkpoint]=====================>>\n"\
               f"[+] ReFS Version: {self.ReFSVersion()}\n"\
               f"[+] Self Descriptor Relative Offset: {self.selfDescriptorOffset()}\n"\
               f"[+] Self Descriptor Length: {self.selfDescriptorLength()}\n"\
               f"[+] Checkpoint Virtual Clock: {self.chkpVirtualClock()}\n"\
               f"[+] Allocator Virtual Clock: {self.allocatorVirtualClock()}\n"\
               f"[+] Oldest Log Record: {self.oldestLogRecordReference()}\n"\
               f"<<==============[Pointers Info and Offsets]==============>>\n"\
               f"[+] Number Of Pointers: {self.pointerCount()}\n"\
               f"[+] Object ID Table: {self.objectIDPointer()}\n"\
               f"[+] Duplicate Object ID Table: {self.objectIDDuplicatePointer()}\n"\
               f"[+] Medium Allocator Table: {self.mediumAllocatorPointer()}\n"\
               f"[+] Container Allocator Table: {self.containerAllocatorPointer()}\n"\
               f"[+] Schema Table: {self.schemaTablePointer()}\n"\
               f"[+] Duplicate Schema Table: {self.schemaTableDuplicatePointer()}\n"\
               f"[+] Parent Child Table: {self.parentChildTablePointer()}\n"\
               f"[+] Block Reference Count Table: {self.blockReferenceCountPointer()}\n"\
               f"[+] Container Table: {self.containerTablePointer()}\n"\
               f"[+] Duplicate Container Table: {self.containerTableDuplicatePointer()}\n"\
               f"[+] Container Index Table: {self.containerIndexTablePointer()}\n"\
               f"[+] Integrity State Table: {self.integrityStateTablePointer()}\n"\
               f"[+] Small Allocator Table: {self.smallAllocatorTablePointer()}\n"\
               f"{PageDescriptor(self.__byteArray[self.selfDescriptorOffset():][:self.selfDescriptorLength()]).info()}"
