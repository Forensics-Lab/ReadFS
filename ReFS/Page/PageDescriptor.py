from typing import Union
from struct import unpack
from Managers.Bytes import Formater

class PageDescriptor:
    def __init__(self, byteArray: Union[list[bytes], tuple[bytes], set[bytes]], clusterSize) -> None:
        self.formater = Formater()
        byteOffset, byteRange = (8, 0x30) if clusterSize == 65536 else (4, 0x2C)
        self.pdStruct = self.formater.removeEmptyEntries(unpack(f"<4qh2bh2p{byteOffset}s", byteArray[:byteRange]))

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
