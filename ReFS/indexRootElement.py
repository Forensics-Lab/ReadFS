from typing import Union
from bytesFormater.formater import Formater

class IndexRootElement:
    def __init__(self, byteArray:Union[list[bytes], tuple[bytes], set[bytes]]) -> None:
        self.byteArray = byteArray
        self.formater = Formater()
    
    def size(self):
        return self.formater.toDecimal(self.byteArray[0x0:0x4])
    
    def rootFixedSize(self):
        return self.formater.toDecimal(self.byteArray[0x4:0x6])
    
    def tableSchema1(self):
        return self.formater.toHex(self.byteArray[0xC:0xE])

    def tableSchema2(self):
        return self.formater.toHex(self.byteArray[0x10:0x12])
    
    def numberOfExtents(self):
        return self.formater.toDecimal(self.byteArray[0x18:0x20])
    
    def tableRowsNumber(self):
        return self.formater.toDecimal(self.byteArray[0x20:0x28])
    
    def variableComponent(self):
        return self.byteArray[0x28:]
    
    def info(self):
        return f"<<=================[Index Root Element]==================>>\n"\
               f"[+] Size: {self.size()} bytes\n"\
               f"[+] Root Fixed Size: {self.rootFixedSize()}\n"\
               f"[+] Table Schema 1: {self.tableSchema1()}\n"\
               f"[+] Table Schema 2: {self.tableSchema2()}\n"\
               f"[+] Number of Extents: {self.numberOfExtents()}\n"\
               f"[+] Table Rows Number: {self.tableRowsNumber()}"