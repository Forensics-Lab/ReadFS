from typing import Union
from bytesFormater.formater import Formater

class PageChecksumData:
    def __init__(self, byteArray:Union[list[bytes], tuple[bytes], set[bytes]]) -> None:
        self.byteArray = byteArray
        self.formater = Formater()

    def checksum(self):
        return self.formater.toHex(self.byteArray)
        # return self.byteArray.

    def info(self):
        return f"<<=================[Page Checksum Data]==================>>\n"\
               f"[+] Page Data Checksum: {self.checksum()}\n"\
               f"<<=======================================================>>" 
