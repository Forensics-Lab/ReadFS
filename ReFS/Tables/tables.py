from typing import Union
from ReFS.Page import PageDescriptor
from bytesReader.bytesFormater import Formater

class Table:
    def __init__(self, byteArray:Union[list[bytes], tuple[bytes], set[bytes]]) -> None:
        self.byteArray = byteArray
        self.formater = Formater()
    
    def tableID(self, val:str) -> str:
        try:
            tableIDNames = self.formater.get_file_contents("ReFS/Identifiers/Tables/tableIdentifiers.json")
            return tableIDNames[str(int(val, 16))]
        except KeyError:
            return "Other directory table"

class Container(Table):
    def __init__(self, byteArray:Union[list[bytes], tuple[bytes], set[bytes]]) -> None:
        super().__init__(byteArray)

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

class ObjectID(Table):
    def __init__(self, byteArray:Union[list[bytes], tuple[bytes], set[bytes]]) -> None:
        super().__init__(byteArray)

    def id(self) -> str:
        return self.tableID(hex(self.formater.toDecimal(self.byteArray[0x8:0x10])))

    def durableLSNOffset(self) -> int:
        return self.formater.toDecimal(self.byteArray[0x18:0x1C])

    def bufferOffset(self) -> int:
        return self.formater.toDecimal(self.byteArray[0x20:0x24])

    def bufferLength(self) -> int:
        return self.formater.toDecimal(self.byteArray[0x24:0x28])

    def durableLSN(self) -> tuple[int, int]:
        LSN = self.byteArray[0x28:0x30]
        LSN0 = self.formater.toDecimal(LSN[0x0:0x4])
        LSN1 = self.formater.toDecimal(LSN[0x4:0x8])
        return LSN0, LSN1

    def pageReference(self) -> tuple[int, int, int, int]:
        return PageDescriptor(self.byteArray[0x30:0xD8]).LCNS()

    def bufferData(self) -> bytearray:
        return self.byteArray[self.bufferOffset():self.bufferOffset() + self.bufferLength()]

    def structure(self) -> dict:
        return {"ID": self.id(),
                "LSN Offset": self.durableLSNOffset(),
                "Buffer Offset": self.bufferOffset(),
                "Buffer Length": self.bufferLength(),
                "Durable LSN": self.durableLSN(),
                "Page Reference":self.pageReference()}

class Schema(Table):
    def __init__(self, byteArray:Union[list[bytes], tuple[bytes], set[bytes]]) -> None:
        super().__init__(byteArray)

    def id(self) -> str:
        return hex(self.formater.toDecimal(self.byteArray[0x0:0x4]))[2:].upper()

    def schemaSize(self) -> int:
        return self.formater.toDecimal(self.byteArray[0x8:0xC][0x0:0x4])

    def schemaOffset(self) -> int:
        return self.formater.toDecimal(self.byteArray[0xC:0x10])

    def schemaLength(self) -> int:
        return self.formater.toDecimal(self.byteArray[0x20:0x24])

    def collation(self) -> int:
        return self.formater.toDecimal(self.byteArray[0x24:0x28])

    def rootNodeSize(self) -> int:
        return self.formater.toDecimal(self.byteArray[0x38:0x3C])

    def indexRootSize(self) -> int:
        return self.formater.toDecimal(self.byteArray[0x3C:0x40])

    def pageSize(self) -> int:
        return self.formater.toDecimal(self.byteArray[0x44:0x48])

    def structure(self) -> dict:
        return {"Schema ID": self.id(),
                "Schema size ": self.schemaSize(),
                "Schema Offset": self.schemaOffset(),
                "Schema Length": self.schemaLength(),
                "Collation": self.collation(),
                "Node Size": self.rootNodeSize(),
                "Page Size": self.pageSize()}

class ParentChild(Table):
    def __init__(self, byteArray:Union[list[bytes], tuple[bytes], set[bytes]]) -> None:
        super().__init__(byteArray)

    def parent(self) -> str:
        return hex(self.formater.toDecimal(self.byteArray[0x8:0xA]))

    def child(self) -> str:
        return hex(self.formater.toDecimal(self.byteArray[0x18:0x20]))

    def structure(self) -> dict:
        return {"Parent ID":f"{self.tableID(self.parent())} ({self.parent()})",
                "Child ID":self.child()}
