from typing import Union, Tuple, List, Set
from struct import unpack
from Managers.Bytes import Formater
from Managers.Handlers import Config

class PageHeader:
    def __init__(self, byteArray: Union[List[bytes], Tuple[bytes], Set[bytes]]) -> None:
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
        identifiersStruct = Config().get_file_contents("ReFS/Identifiers/Tables/tableIdentifiers.json")
        identifier = str(self.phStruct[10] ^ self.phStruct[11])
        return identifiersStruct[identifier] if identifier in identifiersStruct else identifier

    def info(self) -> str:
        LCN_0, LCN_1, LCN_2, LCN_3 = self.LCNS()
        return "<<=====================[Page Header]=====================>>\n"\
               f"[+] Page Signature: {self.pageSignature()}\n"\
               f"[+] Volume Signature: {self.volumeSignature()}\n"\
               f"[+] LCN_0: {LCN_0}\n"\
               f"[+] LCN_1: {LCN_1}\n"\
               f"[+] LCN_2: {LCN_2}\n"\
               f"[+] LCN_3: {LCN_3}\n"\
               f"[+] Table Type: {self.tableIdentifier()}"
