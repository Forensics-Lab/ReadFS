from typing import Union, Tuple, List, Set
from cli.ReFS.Tables import Table

class LogFile(Table):
    def __init__(self, byteArray:Union[List[bytes], Tuple[bytes], Set[bytes]]) -> None:
        super().__init__(byteArray)

    def loggingAreaStart(self):
        return self.formater.toDecimal(self.byteArray[0x0:0x8])

    def loggingAreaEnd(self):
        return self.formater.toDecimal(self.byteArray[0x8:0x10])

    def loggingAreaSize(self):
        return self.formater.toDecimal(self.byteArray[0x10:0x18])

    def restartArea(self):
        return self.formater.toDecimal(self.byteArray[0x18:0x20])

    def restartAreaDub(self):
        return self.formater.toDecimal(self.byteArray[0x20:0x28])

    def structure(self):
        return {"Logging start": self.loggingAreaStart(),
                "Logging end": self.loggingAreaEnd(),
                "Logging size": self.loggingAreaSize(),
                "Restart area": self.restartArea(),
                "Restart area copy": self.restartAreaDub()}
