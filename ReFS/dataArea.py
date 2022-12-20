from typing import Union
from bytesFormater.formater import Formater

class DataArea:
    def __init__(self, byteArray:Union[list[bytes], tuple[bytes], set[bytes]]) -> None:
        self.byteArray = byteArray
        self.formater = Formater()

    def entrySize(self):
        return self.formater.toDecimal(self.byteArray[0x0:0x4])

    def keyStartOffset(self):
        return self.formater.toDecimal(self.byteArray[0x4:0x6])

    def keySize(self):
        return self.formater.toDecimal(self.byteArray[0x6:0x8])

    def flag(self):
        flagsStruct = {0x2:"Rightmost extent in a subtree", 0x4:"Deleted Entry", 0x40:"Stream Index Entry"}
        flagValue = self.formater.toDecimal(self.byteArray[0x8:0xA])
        # return flagsStruct[flagValue]
        return flagValue

    def vlaueStartOffset(self):
        return self.formater.toDecimal(self.byteArray[0xA:0xC])

    def valueSize(self):
        return self.formater.toDecimal(self.byteArray[0xC:0xE])


    def info(self):
        #This needs improvement so please don't use it
        # return self.byteArray
        return f"<<======================[Data Area]======================>>\n"\
               f"[+] Entry Size: {self.entrySize()}\n"\
               f"[+] Key Start Offset: {self.keyStartOffset()}\n"\
               f"[+] Key Size: {self.keySize()}\n"\
               f"[+] Key Type: {self.flag()}\n"\
               f"[+] Value Start Offset: {self.vlaueStartOffset()}\n"\
               f"[+] Value Size: {self.valueSize()}\n"\
               f"<<=======================================================>>"
