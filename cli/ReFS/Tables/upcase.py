from typing import Union, Tuple, List, Set
from cli.ReFS.Tables import Table

class Upcase(Table):
    def __init__(self, byteArray:Union[List[bytes], Tuple[bytes], Set[bytes]]) -> None:
        super().__init__(byteArray)

    def sequenceNumber(self):
        return self.formater.toDecimal(self.byteArray[0x0:0x4])

    def data(self):
        return self.byteArray[0x8:]

    def structure(self):
        return {"Sequence number": self.sequenceNumber(),
                "Data": self.data()}
