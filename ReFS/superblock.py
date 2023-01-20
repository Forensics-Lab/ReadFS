from ReFS.page import *
from typing import Union

class Superblock:
    def __init__(self, byteArray:Union[list[bytes], tuple[bytes], set[bytes]], _formater) -> None:
        self.byteArray = byteArray
        self.pageHeader = PageHeader(self.byteArray[0x0:0x50], _formater)
        self.formater = _formater

    def GUID(self) -> str:
        temp = [self.formater.reverseBytes(self.byteArray[0x50:0x60][i:i+4]) for i in range(0, len(self.byteArray[0x50:0x60]), 4)]
        temp = [self.formater.toDecimal(i) for i in temp]
        sig = (temp[0] ^ temp[1] ^ temp[2] ^ temp[3]).to_bytes(len(temp), "little").hex().upper()
        return sig

    def version(self) -> int:
        return self.formater.toDecimal(self.byteArray[0x68:0x70])

    def checkpointOffset(self) -> tuple[int, int]:
        clusterSize = len(self.byteArray)
        checkpointRelativeOffset = self.formater.toDecimal(self.byteArray[0x70:0x74])
        chk1 = self.formater.toDecimal(self.byteArray[checkpointRelativeOffset:checkpointRelativeOffset+0x08]) * clusterSize
        chk2 = self.formater.toDecimal(self.byteArray[checkpointRelativeOffset+0x08:checkpointRelativeOffset+0x10]) * clusterSize
        return  chk1, chk2

    def checkpointReferenceNumber(self) -> int:
        return self.formater.toDecimal(self.byteArray[0x74:0x78])

    def selfDescriptorOffset(self) -> int:
        return self.formater.toDecimal(self.byteArray[0x78:0x7C])

    def selfDescriptorLength(self) -> int:
        return self.formater.toDecimal(self.byteArray[0x7C:0x80])

    def info(self) -> str:
        checkpoint1, checkpoint2 = self.checkpointOffset()
        return f"{self.pageHeader.info()}\n"\
               f"<<======================[Superblock]=====================>>\n"\
               f"[+] GUID: {self.GUID()}\n"\
               f"[+] Superblock Version: {self.version()}\n"\
               f"[+] Checkpoint Reference Number: {self.checkpointReferenceNumber()}\n"\
               f"[+] Checkpoint1 Offset: {checkpoint1} bytes\n"\
               f"[+] Checkpoint2 Offset: {checkpoint2} bytes\n"\
               f"[+] Self Descriptor Relative Offset: {self.selfDescriptorOffset()} bytes\n"\
               f"[+] Self Descriptor Length: {self.selfDescriptorLength()} bytes\n"\
               f"{PageDescriptor(self.byteArray[self.selfDescriptorOffset():][:self.selfDescriptorLength()], self.formater).info()}"\
