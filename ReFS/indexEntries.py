from typing import Union
from bytesReader.bytesFormater import Formater

class IndexEntries:
    def __init__(self, byteArray:Union[list[bytes], tuple[bytes], set[bytes]], keysCount:int) -> None:
        self.byteArray = byteArray
        self.formater = Formater()
        self.keysCont = keysCount

    def entrySize(self, _bytes: bytes) -> int:
        return self.formater.toDecimal(_bytes[0x0:0x4])

    def keyStartOffset(self, _bytes: bytes) -> int:
        return self.formater.toDecimal(_bytes[0x4:0x6])

    def keySize(self, _bytes: bytes) -> int:
        return self.formater.toDecimal(_bytes[0x6:0x8])

    def flag(self, _bytes: bytes) -> int:
        flagsStruct = {0x0:"Flag Not Set",
                       0x2:"Rightmost extent in a subtree",
                       0x4:"Deleted Entry",
                       0x6:"Rightmost extent in a subtree & Deleted Entry",
                       0x40:"Stream Index Entry"}
        flagValue = self.formater.toDecimal(_bytes[0x8:0xA])
        return flagsStruct[flagValue]

    def vlaueStartOffset(self, _bytes: bytes) -> int:
        return self.formater.toDecimal(_bytes[0xA:0xC])

    def valueSize(self, _bytes: bytes) -> int:
        return self.formater.toDecimal(_bytes[0xC:0xE])

    def _createGeneralEntriesHeader(self, _bytes):
        entryGeneralHeader = {"Entry size": self.entrySize(_bytes),
                              "Key Offset Start":self.keyStartOffset(_bytes),
                              "Key Size":self.keySize(_bytes),
                              "Flag":self.flag(_bytes),
                              "Value Start Offset": self.vlaueStartOffset(_bytes),
                              "Value Size": self.valueSize(_bytes),
                              # "x" Will beed to be replaced to the related table structure of different tables
                              "x": {"Container":self.formater.toDecimal(_bytes[16:][:0x4]),
                                    "Flag":self.formater.toDecimal(_bytes[16:][0x10:0x11]),
                                    "Empty Clusters":1024 - self.formater.toDecimal(_bytes[16:][0x20:0x28]),
                                    "Container LCN": self.formater.toDecimal(_bytes[16:][0xD0:0xD8]),
                                    "Clusters Per Container": self.formater.toDecimal(_bytes[16:][0xD8:0xE0])}}
        return entryGeneralHeader

    def getEntries(self):
        ent = []
        relativeOffset = 0
        for i in range(self.keysCont):
            keySize = self.formater.toDecimal(self.byteArray[i*relativeOffset:i*relativeOffset+0x4])
            key = self.byteArray[i*relativeOffset:i*relativeOffset + keySize]
            ent.append(self._createGeneralEntriesHeader(key))
            relativeOffset = keySize
        return ent
