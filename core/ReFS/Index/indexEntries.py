from core.ReFS.Tables import *
from typing import Union, Tuple, List, Set
from prettytable import PrettyTable
from core.Managers.Bytes import Formater

class IndexEntries:
    def __init__(self, byteArray:Union[List[bytes], Tuple[bytes], Set[bytes]], keysCount:int, tableIdentifier, indexRootvariableComponent:bytes, clusterSize:int) -> None:
        self.formater = Formater()
        self.keysCont = keysCount
        self.byteArray = byteArray
        self.clusterSize = clusterSize
        self.tableIdentifier = tableIdentifier
        self.indexRootvariableComponent = indexRootvariableComponent

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
                              "Key Offset":self.keyStartOffset(_bytes),
                              "Key Size":self.keySize(_bytes),
                              "Flag":self.flag(_bytes),
                              "Value Offset": self.vlaueStartOffset(_bytes),
                              "Value Size": self.valueSize(_bytes),
                              self.tableIdentifier: self.__tableSpecifficStruct(_bytes)}
        return entryGeneralHeader

    def __tableSpecifficStruct(self, _bytes: bytes) -> Union[ObjectID, Schema, ParentChild, Container, Upcase, LogFile]:
        if self.tableIdentifier in ("Object ID", "Object ID (Dup.)"):
            return ObjectID(_bytes[16:], self.clusterSize).structure()
        elif self.tableIdentifier in ("Schema", "Schema (Dup.)"):
            return Schema(_bytes[16:]).structure()
        elif self.tableIdentifier in "Parent Child":
            return ParentChild(_bytes[16:]).structure()
        elif self.tableIdentifier in ("Container", "Container (Dup.)"):
            return Container(_bytes[16:], self.clusterSize).structure()
        elif self.tableIdentifier in ("Upcase", "Upcase (Dup.)"):
            return Upcase(_bytes[16:]).structure()
        elif self.tableIdentifier in ("Logfile Information", "Logfile Information (Dup.)"):
            return LogFile(_bytes[16:]).structure()

    def getEntries(self) -> list:
        ent = []
        relativeOffset = 0
        for _ in range(self.keysCont):
            keySize = self.formater.toDecimal(self.byteArray[relativeOffset:relativeOffset+0x4])
            key = self.byteArray[relativeOffset:relativeOffset + keySize]
            if key:
                ent.append(self.__getKeyValueData(key))
            relativeOffset += keySize
        return tuple(ent)

    def logEntry(self, entry=None):
        # This function will need to be redone but for now it gets the job done.
        entries = self.getEntries()
        table = PrettyTable()
        keys = list(entries[0].keys())
        values = list(entries[0].values())
        table.field_names = ["Nr."] + keys[:-1] + ["Table Type"] + list(values[-1].keys())
        if not entry:
            for idx, ent in enumerate(entries, 1):
                table.add_row([idx] + list(ent.values())[:-1] + [tuple(ent.keys())[-1]] + list(tuple(ent.values())[-1].values()))
        elif entry:
            table.add_row([entry] + list(entries[entry - 1].values())[:-1] + [tuple(entries[entry- 1].keys())[-1]] + list(tuple(entries[entry - 1].values())[-1].values()))
        return table