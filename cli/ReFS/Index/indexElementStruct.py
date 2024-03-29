
from typing import Union, List, Tuple, Set
from cli.Managers.Bytes import Formater

class IndexElement:
    def __init__(self, byteArray:Union[List[bytes], Tuple[bytes], Set[bytes]]) -> None:
        self.byteArray = byteArray
        self.formater = Formater()

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
        return self.byteArray[0x28:self.size() - self.rootFixedSize()]


    def info(self) -> str:
        return f"<<=================[Index Root Element]==================>>\n"\
               f"[+] Size: {self.size()}\n"\
               f"[+] Root Fixed Size: {self.rootFixedSize()}\n"\
               f"[+] Table Schema 1 Identifier: {self.tableSchema1Identifier()}\n"\
               f"[+] Table Schema 2 Identifier: {self.tableSchema2Identifier()}\n"\
               f"[+] Table Rows Number: {self.tableRowsNumber()}\n"\
               f"[+] Number of Extents: {self.numberOfTableExtents()}"
