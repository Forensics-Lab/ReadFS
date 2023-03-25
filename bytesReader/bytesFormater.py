import json

class Formater:
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
    
    def get_file_contents(self, file):
        with open(file, "r") as file:
            data = json.load(file)
        return data
