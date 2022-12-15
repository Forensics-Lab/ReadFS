from typing import Union
from ReFS.pageHeader import PageHeader
from bytesFormater.formater import Formater
from ReFS.pageDescriptor import PageDescriptor

class Checkpoint:
    def __init__(self, byteArray:Union[list[bytes], tuple[bytes], set[bytes]]) -> None:
        self.byteArray = byteArray
        self.formater = Formater()
        self.pageheader = PageHeader(self.byteArray[0x0:0x50])

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
        plist = [self.formater.toDecimal(plist[i:i+4]) for i in range(0, len(plist), 4)]
        return plist

    def objectIDPointer(self) -> int:
        return self.pointerList()[0]

    def mediumAllocatorPointer(self) -> int:
        return self.pointerList()[1]

    def containerAllocatorPointer(self) -> int:
        return self.pointerList()[2]

    def schemaTablePointer(self) -> int:
        return self.pointerList()[3]

    def parentChildTablePointer(self) -> int:
        return self.pointerList()[4]

    def objectIDDuplicatePointer(self) -> int:
        return self.pointerList()[5]

    def blockReferenceCountPointer(self) -> int:
        return self.pointerList()[6]

    def containerTablePointer(self) -> int:
        return self.pointerList()[7]

    def containerTableDuplicatePointer(self) -> int:
        return self.pointerList()[8]

    def schemaTableDuplicatePointer(self) -> int:
        return self.pointerList()[9]

    def containerIndexTablePointer(self) -> int:
        return self.pointerList()[10]

    def integrityStateTablePointer(self) -> int:
        return self.pointerList()[11]

    def smallAllocatorTablePointer(self) -> int:
        return self.pointerList()[12]

    def info(self) -> str:
        return f"{self.pageheader.info()}\n"\
               f"<<======================[Checkpoint]=====================>>\n"\
               f"[+] ReFS Version: {self.majorVersion()}.{self.minorVersion()}\n"\
               f"[+] Self Descriptor Relative Offset: {self.selfDescriptorOffset()}\n"\
               f"[+] Self Descriptor Length: {self.selfDescriptorLength()}\n"\
               f"[+] Checkpoint Virtual Clock: {self.chkpVirtualClock()}\n"\
               f"[+] Allocator Virtual Clock: {self.allocatorVirtualClock()}\n"\
               f"[+] Oldest Log Record: {self.oldestLogRecordReference()}\n"\
               f"[+] Alignment: {self.alignment()}\n"\
               f"[+] Reserved: {self.reserved()}\n"\
               f"<<================[Pointers Offset Info]=================>>\n"\
               f"[+] Count: {self.pointerCount()}\n"\
               f"[+] Object ID Table: {self.objectIDPointer()} bytes\n"\
               f"[+] Duplicate Object ID Table: {self.objectIDDuplicatePointer()} bytes\n"\
               f"[+] Medium Allocator Table: {self.mediumAllocatorPointer()} bytes\n"\
               f"[+] Container Allocator Table: {self.containerAllocatorPointer()} bytes\n"\
               f"[+] Schema Table: {self.schemaTablePointer()} bytes\n"\
               f"[+] Duplicate Schema Table: {self.schemaTableDuplicatePointer()} bytes\n"\
               f"[+] Parent Child Table: {self.parentChildTablePointer()} bytes\n"\
               f"[+] Block Reference Count Table: {self.blockReferenceCountPointer()} bytes\n"\
               f"[+] Container Table: {self.containerTablePointer()} bytes\n"\
               f"[+] Duplicate Container Table: {self.containerTablePointer()} bytes\n"\
               f"[+] Container Index Table: {self.containerIndexTablePointer()} bytes\n"\
               f"[+] Integrity State Table: {self.integrityStateTablePointer()} bytes\n"\
               f"[+] Small Allocator Table: {self.smallAllocatorTablePointer()} bytes\n"\
               f"{PageDescriptor(self.byteArray[self.selfDescriptorOffset():][:self.selfDescriptorLength()]).info()}"
