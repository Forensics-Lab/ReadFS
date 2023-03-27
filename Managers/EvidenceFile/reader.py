from ..Bytes import Formater

class Reader():
    def __init__(self, file: str) -> None:
        self.file = file
        self.formater = Formater()

    def getBytes(self, byteRange: int = 65536, offset: int= 0) -> bytes:
        with open(self.file, "rb") as file:
            file.seek(offset)
            data = file.read(byteRange)
        return data
