from typing import Union
from bytesReader.bytesFormater import Formater

class IndexElement:
    def __init__(self, byteArray:Union[list[bytes], tuple[bytes], set[bytes]]) -> None:
        self.byteArray = byteArray
        self.formater = Formater()

    def size(self) -> int:
        return self.formater.toDecimal(self.byteArray[0x0:0x4])

class IndexRootElement(IndexElement):
    def __init__(self, byteArray: Union[list[bytes], tuple[bytes], set[bytes]]) -> None:
        super().__init__(byteArray)
    
    def rootFixedSize(self) -> int:
        return self.formater.toDecimal(self.byteArray[0x4:0x6])
    
    def tableSchema1Identifier(self) -> str:
        return self.formater.toHex(self.byteArray[0xC:0xE])

    def tableSchema2Identifier(self) -> str:
        return self.formater.toHex(self.byteArray[0x10:0x12])
    
    def numberOfTableExtents(self) -> int:
        return self.formater.toDecimal(self.byteArray[0x18:0x20])

    def tableRowsNumber(self) -> int:
        return self.formater.toDecimal(self.byteArray[0x20:0x28])

    def variableComponent(self) -> bytes:
        variableComponentSize = self.size() - self.rootFixedSize()
        return self.byteArray[0x28:variableComponentSize]

    def _rootIndexType(self) -> str:
        return 

    def _nonRootIndexType(self) -> str:
        return f"[+] Root Fixed Size: {self.rootFixedSize()}"

    def info(self) -> str:
        return f"<<=================[Index Root Element]==================>>\n"\
               f"[+] Size: {self.size()}\n"\
               f"[+] Root Fixed Size: {self.rootFixedSize()}\n"\
               f"[+] Table Schema 1 Identifier: {self.tableSchema1Identifier()}\n"\
               f"[+] Table Schema 2 Identifier: {self.tableSchema2Identifier()}\n"\
               f"[+] Table Rows Number: {self.tableRowsNumber()}\n"\
               f"[+] Number of Extents: {self.numberOfTableExtents()}"

class IndexNonRootElement(IndexElement):
    def __init__(self, byteArray: Union[list[bytes], tuple[bytes], set[bytes]]) -> None:
        super().__init__(byteArray)
    
    def alignment(self) -> bytes:
        return self.byteArray[0x4:0x8]
    
    def info(self) -> str:
        return f"<<===============[Index Non-Root Element]================>>\n"\
               f"[+] Size: {self.size()}"