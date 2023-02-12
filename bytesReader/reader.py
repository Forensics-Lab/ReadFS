from typing import Union
from .bytesFormater import Formater

class Reader():
    def __init__(self, file: str) -> None:
        self.file = file
        self.formater = Formater()

    def getBytes(self, byteRange: Union[list[bytes, int], tuple[bytes, int], set[bytes, int]], offset: Union[int, bytes] = 0) -> bytes:
        with open(self.file, "rb") as file:
            file.seek(offset + byteRange[0])
            data = file.read(abs(byteRange[0] - byteRange[1]))
        return data