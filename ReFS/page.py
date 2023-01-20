from typing import Union

class PageHeader:
    def __init__(self, byteArray:Union[list[bytes], tuple[bytes], set[bytes]], _formater) -> None:
        self.byteArray = byteArray
        self.formater = _formater

    def pageSignature(self) -> str:
        return self.formater.toString(self.byteArray[0x0:0x4])

    def always2(self) -> int:
        return self.formater.toDecimal(self.byteArray[0x4:0x8])

    def always0(self) -> int:
        return self.formater.toDecimal(self.byteArray[0x8:0xC])

    def volumeSignature(self) -> str:
        return self.formater.toHex(self.byteArray[0xC:0x10])

    def virtualAllocatorClock(self) -> str:
        return self.formater.toHex(self.byteArray[0x10:0x18])

    def treeUpdateClock(self) -> str:
        return self.formater.toHex(self.byteArray[0x18:0x20])

    def LCNS(self) -> list:
        LCN_0 = self.formater.toDecimal(self.byteArray[0x20:0x28])
        LCN_1 = self.formater.toDecimal(self.byteArray[0x28:0x30])
        LCN_2 = self.formater.toDecimal(self.byteArray[0x30:0x38])
        LCN_3 = self.formater.toDecimal(self.byteArray[0x38:0x40])
        return LCN_0, LCN_1, LCN_2, LCN_3

    def tableIdentifier(self) -> str:
        identifiersStruct = {0x2: "Object ID",
                             0x21: "Medium Allocator",
                             0x20: "Container Allocator",
                             0x1: "Schema",
                             0x3: "Parent Child",
                             0x4: "Object ID (Duplicate)",
                             0x5: "Block Reference Count",
                             0xB: "Container",
                             0xC: "Container (Duplicate)",
                             0x6: "Schema (Duplicate)",
                             0xE: "Container Index",
                             0xF: "Integrity State",
                             0x22: "Small Allocator"}

        high = self.formater.toDecimal(self.byteArray[0x40:0x48])
        low = self.formater.toDecimal(self.byteArray[0x48:0x50])
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
    def __init__(self, byteArray:Union[list[bytes], tuple[bytes], set[bytes]], _formater) -> None:
        self.byteArray = byteArray
        self.formater = _formater

    def LCNS(self) -> list:
        LCN_0 = self.formater.toDecimal(self.byteArray[0x0:0x08])
        LCN_1 = self.formater.toDecimal(self.byteArray[0x08:0x10])
        LCN_2 = self.formater.toDecimal(self.byteArray[0x10:0x18])
        LCN_3 = self.formater.toDecimal(self.byteArray[0x18:0x20])
        return LCN_0, LCN_1, LCN_2, LCN_3

    def checksumType(self) -> str:
        chkt = self.formater.toDecimal(self.byteArray[0x22:0x23])
        return "CRC32-C" if chkt == 1 else "CRC64-ECMA-182"
    
    def checksumOffset(self):
        return self.formater.toDecimal(self.byteArray[0x23:0x24])
    
    def checksumLength(self) -> int:
        return self.formater.toDecimal(self.byteArray[0x24:0x26])

    def info(self) -> str:
        LCN_0, LCN_1, LCN_2, LCN_3 = self.LCNS() 
        return f"<<================[Self Page Descriptor]=================>>\n"\
               f"[+] LCN_0: {LCN_0}\n"\
               f"[+] LCN_1: {LCN_1}\n"\
               f"[+] LCN_2: {LCN_2}\n"\
               f"[+] LCN_3: {LCN_3}\n"\
               f"[+] Checksum Type: {self.checksumType()}\n"\
               f"[+] Checksum Offset: {self.checksumOffset()}\n"\
               f"[+] Checksum Length: {self.checksumLength()}\n"\
               f"{PageChecksumData(self.byteArray[0x20 + self.checksumOffset():][:self.checksumLength()], self.formater).info()}"

class PageChecksumData:
    def __init__(self, byteArray:Union[list[bytes], tuple[bytes], set[bytes]], _formater) -> None:
        self.byteArray = byteArray
        self.formater = _formater

    def checksum(self) -> str:
        return self.formater.toHex(self.byteArray)

    def info(self) -> str:
        return f"<<=================[Page Data Checksum]==================>>\n"\
               f"[+] Page Data Checksum: {self.checksum()}\n"\
               f"<<=======================================================>>" 
