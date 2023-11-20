from typing import Union, Tuple, List, Set
from cli.ReFS.Tables import Table
from cli.ReFS.Page import PageDescriptor

class ObjectID(Table):
    def __init__(self, byteArray:Union[List[bytes], Tuple[bytes], Set[bytes]], clusterSize) -> None:
        super().__init__(byteArray)
        self.clusterSize = clusterSize

    def id(self) -> str:
        return self.tableID(hex(self.formater.toDecimal(self.byteArray[0x8:0x10])))

    def durableLSNOffset(self) -> int:
        return self.formater.toDecimal(self.byteArray[0x18:0x1C])

    def bufferOffset(self) -> int:
        return self.formater.toDecimal(self.byteArray[0x20:0x24])

    def bufferLength(self) -> int:
        return self.formater.toDecimal(self.byteArray[0x24:0x28])

    def durableLSN(self) -> Tuple[int, int]:
        LSN = self.byteArray[0x28:0x30]
        LSN0 = self.formater.toDecimal(LSN[0x0:0x4])
        LSN1 = self.formater.toDecimal(LSN[0x4:0x8])
        return LSN0, LSN1

    def pageReference(self) -> Tuple[int, int, int, int]:
        return PageDescriptor(self.byteArray[0x30:0xD8], self.clusterSize).LCNS()

    def bufferData(self) -> bytearray:
        return self.byteArray[self.bufferOffset():self.bufferOffset() + self.bufferLength()]

    def structure(self) -> dict:
        return {"ID": self.id(),
                "LSN Offset": self.durableLSNOffset(),
                "Buffer Offset": self.bufferOffset(),
                "Buffer Length": self.bufferLength(),
                "Durable LSN": self.durableLSN(),
                "Page Reference":self.pageReference()}
