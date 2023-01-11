from typing import Union


class IndexRootElement:
    def __init__(self, byteArray:Union[list[bytes], tuple[bytes], set[bytes]], _formater, indexType:int=2) -> None:
        self.byteArray = byteArray
        self.formater = _formater
        self.indexType = indexType

    def size(self) -> int:
        return self.formater.toDecimal(self.byteArray[0x0:0x4])

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
        return f"[+] Root Fixed Size: {self.rootFixedSize()}\n"\
               f"[+] Table Schema 1 Identifier: {self.tableSchema1Identifier()}\n"\
               f"[+] Table Schema 2 Identifier: {self.tableSchema2Identifier()}\n"\
               f"[+] Table Rows Number: {self.tableRowsNumber()}\n"\
               f"[+] Number of Extents: {self.numberOfTableExtents()}"

    def _nonRootIndexType(self) -> str:
        return f"[+] Root Fixed Size: {self.rootFixedSize()}"

    def info(self) -> str:
        indexRootElementInfo = self._rootIndexType() if self.indexType == 2 else self._nonRootIndexType()
        return f"<<=================[Index Root Element]==================>>\n"\
               f"[+] Size: {self.size()}\n"\
               f"{indexRootElementInfo}"