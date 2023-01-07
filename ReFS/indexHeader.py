from typing import Union
from bytesFormater.formater import Formater

class IndexHeader:
    def __init__(self, byteArray:Union[list[bytes], tuple[bytes], set[bytes]]) -> None:
        self.byteArray = byteArray
        self.formater = Formater()

    def dataAreaOffsetStart(self) -> int:
        return self.formater.toDecimal(self.byteArray[0x0:0x4])

    def dataAreaOffsetEnd(self) -> int:
        return self.formater.toDecimal(self.byteArray[0x4:0x8])

    def nodesFreeBytes(self) -> int:
        return self.formater.toDecimal(self.byteArray[0x8:0xC])

    def nodeHeight(self) -> int:
        return self.formater.toDecimal(self.byteArray[0xC:0xD])

    def flag(self) -> str:
        flagsStruct = {0x1:"Iner", 0x2:"Root", 0x4:"Stream"}
        flagValue = self.formater.toDecimal(self.byteArray[0xD:0xE])
        return flagsStruct[flagValue]

    def keyIndexStart(self) -> int:
        return self.formater.toDecimal(self.byteArray[0x10:0x14])

    def keyIndexEntries(self) -> int:
        return self.formater.toDecimal(self.byteArray[0x14:0x18])

    def keyIndexEnd(self) -> int:
        return self.formater.toDecimal(self.byteArray[0x20:0x24])

    def info(self) -> str:
        return f"<<====================[Index Header]=====================>>\n"\
               f"[+] Node Type: {self.flag()}\n"\
               f"[+] Node Height: {self.nodeHeight()}\n"\
               f"[+] Start Of Data Area: {self.dataAreaOffsetStart()}\n"\
               f"[+] End Of Data Area: {self.dataAreaOffsetEnd()}\n"\
               f"[+] Key Index Start: {self.keyIndexStart()}\n"\
               f"[+] Key Index End: {self.keyIndexEnd()}\n"\
               f"[+] Key Index Entries: {self.keyIndexEntries()}\n"\
               f"[+] Node Free Bytes: {self.nodesFreeBytes()}\n"\
               f"<<=======================================================>>" 