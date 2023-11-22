from typing import Union, Tuple, List, Set
from struct import unpack
from core.Managers.Bytes import Formater


class PageVerifySelfChecksum:
    class checksum_type: CRC32C = 1; CRC64_ECMA_182 = 2

    def __init__(self, data: bytes, type=checksum_type.CRC32C):
        from crc import Calculator, Configuration

        CRC32C = Configuration(
            width=32,
            polynomial=0x1EDC6F41,
            init_value=0xFFFFFFFF,
            final_xor_value=0xFFFFFFFF,
            reverse_input=True,
            reverse_output=True,
        )

        CRC64_ECMA_182 = Configuration(
            width=64,
            polynomial=0x9A6C9329AC4BC9B5,
            init_value=0x0000000000000000,
            final_xor_value=0x0000000000000000,
            reverse_input=False,
            reverse_output=False,
        )

        self.__crcCfg = CRC32C if (type == 1) else CRC64_ECMA_182

        self.calculator = Calculator(self.__crcCfg)

        self._checksum = self.calculator.checksum(data)

    def checksum(self): return self._checksum.to_bytes(length=int(self.__crcCfg.width / 8), byteorder='little')


class PageDescriptor:
    def __init__(self, byteArray: Union[List[bytes], Tuple[bytes], Set[bytes]], clusterSize) -> None:
        self.formater = Formater()
        byteOffset, byteRange = (8, 0x30) if clusterSize == 65536 else (4, 0x2C)
        self.pdStruct = self.formater.removeEmptyEntries(unpack(f"<4qh2bh2p{byteOffset}s", byteArray[:byteRange]))

    def LCNS(self) -> Tuple[int, int, int, int]:
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
