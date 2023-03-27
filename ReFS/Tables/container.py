from typing import Union
from ReFS.Tables import Table

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