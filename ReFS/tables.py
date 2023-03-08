from typing import Union
from ReFS.page import PageDescriptor
from bytesReader.bytesFormater import Formater

class Container:
    def __init__(self, byteArray:Union[list[bytes], tuple[bytes], set[bytes]]) -> None:
        self.byteArray = byteArray
        self.formater = Formater()

    def containerNumber(self) -> int:
        return self.formater.toDecimal(self.byteArray[0x0:0x4])

    def flag(self) -> str:
        flagStruct = {0x1: "Inner", 0x2: "Root", 0x4: "Stream"}
        flagValue = self.formater.toDecimal(self.byteArray[0x10:0x11])
        return flagStruct[flagValue]

    def emptyClusters(self) -> int:
        return self.formater.toDecimal(self.byteArray[0x20:0x28])

    def containerLCN(self) -> int:
        return self.formater.toDecimal(self.byteArray[0xD0:0xD8])

    def clustersPerContainer(self) -> int:
        return self.formater.toDecimal(self.byteArray[0xD8:0xE0])

    def structure(self) -> dict:
        return {"Container":self.containerNumber(),
                "Node Type":self.flag(),
                "Empty Clusters":self.clustersPerContainer() - self.emptyClusters(),
                "Container LCN": self.containerLCN(),
                "Clusters Per Container": self.clustersPerContainer()}

class ObjectID:
    def __init__(self, byteArray:Union[list[bytes], tuple[bytes], set[bytes]]) -> None:
        self.byteArray = byteArray
        self.formater = Formater()

    def id(self):
        try:
            tableID = self.formater.toDecimal(self.byteArray[0x8:0x10])
            tableIDNames = {0x7: "Upcase",
                    0x8: "Upcase dup.",
                    0x9: "Logfile Information",
                    0xA: "Logfile Information dup.",
                    0xD: "Trash Stream",
                    0x500: "Volume Information",
                    0x501: "Volume Information dup.",
                    0x520: "File System Metadata",
                    0x530: "Security",
                    0x540: "Reparse Index",
                    0x541: "Reparse Index dup.",
                    0x520: "File System Metadata",
                    0x600: "Root Directory"}
            return tableIDNames[tableID]
        except KeyError:
            return "Other directory table"

    def durableLSNOffset(self):
        return self.formater.toDecimal(self.byteArray[0x18:0x1C])

    def bufferOffset(self):
        return self.formater.toDecimal(self.byteArray[0x20:0x24])

    def bufferLength(self):
        return self.formater.toDecimal(self.byteArray[0x24:0x28])

    def durableLSN(self):
        LSN = self.byteArray[0x28:0x30]
        LSN0 = self.formater.toDecimal(LSN[0x0:0x4])
        LSN1 = self.formater.toDecimal(LSN[0x4:0x8])
        return LSN0, LSN1

    def pageReference(self):
        return PageDescriptor(self.byteArray[0x30:0xD8]).LCNS()

    def bufferData(self):
        return self.byteArray[self.bufferOffset():self.bufferOffset() + self.bufferLength()]

    def structure(self):
        return {"ID": self.id(),
                "LSN Offset": self.durableLSNOffset(),
                "Buffer Offset": self.bufferOffset(),
                "Buffer Length": self.bufferLength(),
                "Durable LSN": self.durableLSN(),
                "Page Reference":self.pageReference()}

class Schema:
    def __init__(self, byteArray:Union[list[bytes], tuple[bytes], set[bytes]]) -> None:
        self.byteArray = byteArray
        self.formater = Formater()

    def id(self):
        return hex(self.formater.toDecimal(self.byteArray[0x0:0x4]))[2:].upper()
    
    def schemaSize(self):
        return self.formater.toDecimal(self.byteArray[0x8:0xC][0x0:0x4])

    def schemaOffset(self):
        return self.formater.toDecimal(self.byteArray[0xC:0x10])

    def schemaLength(self):
        return self.formater.toDecimal(self.byteArray[0x20:0x24])
    
    def collation(self):
        return self.formater.toDecimal(self.byteArray[0x24:0x28])
    
    def rootNodeSize(self):
        return self.formater.toDecimal(self.byteArray[0x38:0x3C])
    
    def indexRootSize(self):
        return self.formater.toDecimal(self.byteArray[0x3C:0x40])

    def pageSize(self):
        return self.formater.toDecimal(self.byteArray[0x44:0x48])

    def structure(self):
        return {"Schema ID": self.id(),
                "Schema size ": self.schemaSize(),
                "Schema Offset": self.schemaOffset(),
                "Schema Length": self.schemaLength(),
                "Collation": self.collation(),
                "Node Size": self.rootNodeSize(),
                "Page Size": self.pageSize()}
