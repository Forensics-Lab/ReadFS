from typing import Union
from bytesFormater.formater import Formater

class PageHeader:
    def __init__(self, byteArray:Union[list[bytes], tuple[bytes], set[bytes]]) -> None:
        self.byteArray = byteArray
        self.formater = Formater()

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

    def LCNS(self):
        LCN_0 = self.formater.toDecimal(self.byteArray[0x20:0x28])
        LCN_1 = self.formater.toDecimal(self.byteArray[0x28:0x30])
        LCN_2 = self.formater.toDecimal(self.byteArray[0x30:0x38])
        LCN_3 = self.formater.toDecimal(self.byteArray[0x38:0x40])
        return LCN_0, LCN_1, LCN_2, LCN_3

    def tableIdentifier(self) -> tuple[int, int]:
        high = self.formater.toDecimal(self.byteArray[0x40:0x48]) 
        low = self.formater.toDecimal(self.byteArray[0x48:0x50])
        return high, low

    def info(self):
        LCN_0,LCN_1,LCN_2,LCN_3 = self.LCNS()
        high, low = self.tableIdentifier()
        return "<<=====================Page Header=====================>>\n"\
               f"[+] Page Signature: {self.pageSignature()}\n"\
               f"[+] Volume Signature: {self.volumeSignature()}\n"\
               f"[+] LCN_0: {LCN_0} cluster\n"\
               f"[+] LCN_1: {LCN_1} cluster\n"\
               f"[+] LCN_2: {LCN_2} cluster\n"\
               f"[+] LCN_3: {LCN_3} cluster\n"\
               f"[+] Table Identifier Low: {low}\n"\
               f"[+] Table Identifier High: {high}"
