from typing import Union
from bytesReader.bytesFormater import Formater

class Container:
    def __init__(self, byteArray:Union[list[bytes], tuple[bytes], set[bytes]]) -> None:
        self.byteArray = byteArray
        self.formater = Formater()
    
    def containerNumber(self):
        return self.formater.toDecimal(self.byteArray[0x0:0x4])

    def flag(self):
        flagStruct = {0x1: "Inner", 0x2: "Root", 0x4: "Stream"}
        flagValue = self.formater.toDecimal(self.byteArray[0x10:0x11])
        return flagStruct[flagValue]

    def emptyClusters(self):
        return self.formater.toDecimal(self.byteArray[0x20:0x28])
    
    def containerLCN(self):
        return self.formater.toDecimal(self.byteArray[0xD0:0xD8])
    
    def clustersPerContainer(self):
        return self.formater.toDecimal(self.byteArray[0xD8:0xE0])

    def structure(self):
        return {"Container":self.containerNumber(),
                "Node Type":self.flag(),
                "Empty Clusters":self.clustersPerContainer() - self.emptyClusters(),
                "Container LCN": self.containerLCN(),
                "Clusters Per Container": self.clustersPerContainer()}