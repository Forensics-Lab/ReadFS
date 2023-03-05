from typing import Union
from ReFS.tables import *
from bytesReader.bytesFormater import Formater

class IndexEntries:
    def __init__(self, byteArray:Union[list[bytes], tuple[bytes], set[bytes]], keysCount:int, tableIdentifier) -> None:
        self.formater = Formater()
        self.keysCont = keysCount
        self.byteArray = byteArray
        self.tableIdentifier = tableIdentifier

    def entrySize(self, _bytes: bytes) -> int:
        return self.formater.toDecimal(_bytes[0x0:0x4])

    def keyStartOffset(self, _bytes: bytes) -> int:
        return self.formater.toDecimal(_bytes[0x4:0x6])

    def keySize(self, _bytes: bytes) -> int:
        return self.formater.toDecimal(_bytes[0x6:0x8])

    def flag(self, _bytes: bytes) -> int:
        flagsStruct = {0x0:"Not Set",
                       0x2:"Rightmost extent in a subtree",
                       0x4:"Deleted Entry",
                       0x6:"Rightmost extent in a subtree & Deleted Entry"}
        flagValue = self.formater.toDecimal(_bytes[0x8:0xA])
        return flagsStruct[flagValue]

    def vlaueStartOffset(self, _bytes: bytes) -> int:
        return self.formater.toDecimal(_bytes[0xA:0xC])

    def valueSize(self, _bytes: bytes) -> int:
        return self.formater.toDecimal(_bytes[0xC:0xE])

    def __getKeyValueData(self, _bytes) -> dict:
        entryGeneralHeader = {"Entry size": self.entrySize(_bytes),
                              "Key Offset Start":self.keyStartOffset(_bytes),
                              "Key Size":self.keySize(_bytes),
                              "Flag":self.flag(_bytes),
                              "Value Start Offset": self.vlaueStartOffset(_bytes),
                              "Value Size": self.valueSize(_bytes),
                              self.tableIdentifier: self.__tableSpecifficStruct(_bytes)}
        return entryGeneralHeader

    def __tableSpecifficStruct(self, _bytes: bytes) -> Union[Container, ObjectID]:
        if self.tableIdentifier == "Container" or self.tableIdentifier == "Container (Duplicate)":
            return Container(_bytes[16:]).structure()
        elif self.tableIdentifier == "Object ID" or self.tableIdentifier == "Object ID (Duplicate)":
            return ObjectID(_bytes[16:]).structure()

    def getEntries(self) -> list:
        ent = []
        relativeOffset = 0
        for _ in range(self.keysCont - 1):
            keySize = self.formater.toDecimal(self.byteArray[relativeOffset:relativeOffset+0x4])
            relativeOffset += keySize
            key = self.byteArray[relativeOffset:relativeOffset + keySize]
            ent.append(self.__getKeyValueData(key))
        return tuple(ent)
