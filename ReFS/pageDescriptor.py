from typing import Union
from ReFS.pageChecksum import PageChecksumData

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