from typing import Union
from cli.ReFS.Tables import Table

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