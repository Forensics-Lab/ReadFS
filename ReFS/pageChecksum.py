from typing import Union


class PageChecksumData:
    def __init__(self, byteArray:Union[list[bytes], tuple[bytes], set[bytes]], _formater) -> None:
        self.byteArray = byteArray
        self.formater = _formater

    def checksum(self) -> str:
        return self.formater.toHex(self.byteArray)

    def info(self) -> str:
        return f"<<=================[Page Data Checksum]==================>>\n"\
               f"[+] Page Data Checksum: {self.checksum()}\n"\
               f"<<=======================================================>>" 
