
class Formater():
    def toDecimal(self, _bytes: bytes, order: str = "little") -> int:
        return int.from_bytes(_bytes, order)
    
    def toString(self, _bytes: bytes) -> str:
        return _bytes.decode()
    
    def toHex(self, _bytes: bytes) -> str:
        return ' '.join([_bytes.hex()[i:i+2] for i in range(len(_bytes))]).upper()
