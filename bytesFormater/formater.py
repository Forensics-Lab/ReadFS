from typing import Union

class Formater():
    def __init__(self, file: str) -> None:
        self.file = file
        self.continerSize = None

    def getBytes(self, byteRange: Union[list[bytes, int], tuple[bytes, int], set[bytes, int]], offset: Union[int, bytes] = 0) -> bytes:
        with open(self.file, "rb") as file:
            file.seek(offset + byteRange[0])
            data = file.read(abs(byteRange[0] - byteRange[1]))
        return data

    def toDecimal(self, _bytes: bytes, order: str = "little") -> int:
        return int.from_bytes(_bytes, order)

    def toString(self, _bytes: bytes) -> str:
        return _bytes.decode()

    def reverseBytes(self, _bytes: bytes) -> bytearray:
        temp = bytearray(_bytes)
        temp.reverse()
        return temp

    def toHex(self, _bytes: bytes) -> str:
        return self.reverseBytes(_bytes).hex().upper()
