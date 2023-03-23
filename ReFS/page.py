from typing import Union
from struct import unpack
from bytesReader.bytesFormater import Formater

class PageHeader:
    def __init__(self, byteArray:Union[list[bytes], tuple[bytes], set[bytes]]) -> None:
        self.formater = Formater()
        self.phStruct = unpack("<4s2i4s8s8s6q", byteArray)

    def pageSignature(self) -> str:
        return self.formater.toString(self.phStruct[0])

    def always2(self) -> int:
        return self.phStruct[1]

    def always0(self) -> int:
        return self.phStruct[2]

    def volumeSignature(self) -> str:
        return self.formater.toHex(self.phStruct[3])

    def virtualAllocatorClock(self) -> str:
        return self.formater.toHex(self.phStruct[4])

    def treeUpdateClock(self) -> str:
        return self.formater.toHex(self.phStruct[5])

    def LCNS(self) -> list:
        return self.phStruct[6:10]

    def tableIdentifier(self) -> str:
        identifiersStruct = {0x2: "Object ID",
                             0x21: "Medium Allocator",
                             0x20: "Container Allocator",
                             0x1: "Schema",
                             0x3: "Parent Child",
                             0x4: "Object ID (Dup.)",
                             0x5: "Block Reference Count",
                             0xB: "Container",
                             0xC: "Container (Dup.)",
                             0x6: "Schema (Dup.)",
                             0xE: "Container Index",
                             0xF: "Integrity State",
                             0x22: "Small Allocator"}

        high = self.phStruct[10]
        low = self.phStruct[11]
        identifier = high + low
        return identifiersStruct[identifier] if identifier in identifiersStruct else "Not A Table"

    def info(self) -> str:
        LCN_0,LCN_1,LCN_2,LCN_3 = self.LCNS()
        return "<<=====================[Page Header]=====================>>\n"\
               f"[+] Page Signature: {self.pageSignature()}\n"\
               f"[+] Volume Signature: {self.volumeSignature()}\n"\
               f"[+] LCN_0: {LCN_0}\n"\
               f"[+] LCN_1: {LCN_1}\n"\
               f"[+] LCN_2: {LCN_2}\n"\
               f"[+] LCN_3: {LCN_3}\n"\
               f"[+] Table Type: {self.tableIdentifier()}"

class PageDescriptor:
    def __init__(self, byteArray:Union[list[bytes], tuple[bytes], set[bytes]]) -> None:
        self.pdStruct = tuple(filter(lambda b: b != b'', unpack("<4qh2bh2p8s", byteArray[:0x30])))
        self.formater = Formater()

    def LCNS(self) -> tuple[int, int, int, int]:
        return self.pdStruct[:4]

    def checksumType(self) -> str:
        chkt = self.pdStruct[5]
        return "CRC32-C" if chkt == 1 else "CRC64-ECMA-182"
    
    def checksumOffset(self):
        return self.pdStruct[6]
    
    def checksumLength(self) -> int:
        return self.pdStruct[7]

    def checksum(self) -> str:
        return self.formater.toHex(self.pdStruct[8])

    def info(self) -> str:
        LCN_0, LCN_1, LCN_2, LCN_3 = self.LCNS() 
        return f"<<================[Self Page Descriptor]=================>>\n"\
               f"[+] LCN_0: {LCN_0}\n"\
               f"[+] LCN_1: {LCN_1}\n"\
               f"[+] LCN_2: {LCN_2}\n"\
               f"[+] LCN_3: {LCN_3}\n"\
               f"<<=================[Page Checksum Info]==================>>\n"\
               f"[+] Checksum Type: {self.checksumType()}\n"\
               f"[+] Checksum Offset: {self.checksumOffset()}\n"\
               f"[+] Checksum Length: {self.checksumLength()}\n"\
               f"[+] Page Checksum: {self.checksum()}\n"\
               f"<<=======================================================>>"
               
