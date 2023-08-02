from cli.ReFS.Page import *
from struct import unpack
from cli.Managers.Bytes import Formater

class Superblock():
    def __init__(self, _bytes: bytes) -> None:
        self.__byteArray = _bytes
        self.formater = Formater()
        self.clusterSize = len(self.__byteArray)
        self.suStruct = self.formater.removeEmptyEntries(unpack("<80s4L8pq4i", self.__byteArray[:0x80]))

    def GUID(self) -> str:
        return self.formater.toHex((self.suStruct[1] ^ self.suStruct[2] ^ self.suStruct[3] ^ self.suStruct[4]).to_bytes(4, "little"))

    def version(self) -> int:
        return self.suStruct[5]

    def checkpointOffset(self) -> tuple[int, int]:
        checkpointRelativeOffset = self.suStruct[6]
        chk1 = self.formater.toDecimal(self.__byteArray[checkpointRelativeOffset:checkpointRelativeOffset+0x08]) * self.clusterSize
        chk2 = self.formater.toDecimal(self.__byteArray[checkpointRelativeOffset+0x08:checkpointRelativeOffset+0x10]) * self.clusterSize
        return  chk1, chk2

    def checkpointReferenceNumber(self) -> int:
        return self.suStruct[7]

    def selfDescriptorOffset(self) -> int:
        return self.suStruct[8]

    def selfDescriptorLength(self) -> int:
        return self.suStruct[9]

    def info(self) -> str:
        checkpoint1, checkpoint2 = self.checkpointOffset()
        return f"{PageHeader(self.suStruct[0]).info()}\n"\
               f"<<======================[Superblock]=====================>>\n"\
               f"[+] GUID: {self.GUID()}\n"\
               f"[+] Superblock Version: {self.version()}\n"\
               f"[+] Checkpoint Reference Number: {self.checkpointReferenceNumber()}\n"\
               f"[+] Checkpoint1 Offset: {checkpoint1} bytes\n"\
               f"[+] Checkpoint2 Offset: {checkpoint2} bytes\n"\
               f"[+] Self Descriptor Relative Offset: {self.selfDescriptorOffset()} bytes\n"\
               f"[+] Self Descriptor Length: {self.selfDescriptorLength()} bytes\n"\
               f"{PageDescriptor(self.__byteArray[self.selfDescriptorOffset():][:self.selfDescriptorLength()], self.clusterSize).info()}"
