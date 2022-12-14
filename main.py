from json5 import load
from typing import Union
from ReFS.bootsector import BootSector

def getBytes(byteRange: Union[list[bytes, int], tuple[bytes, int], set[bytes, int]], offset: Union[int, bytes] = 0) -> bytes:
    path = "D:\\Uni\\Third Year\\CTS3510 Memory Analysis\\samples\\testingAlone\\refs_lo.001"
    with open(path, "rb") as file:
        file.seek(offset+ byteRange[0])
        data = file.read(abs(byteRange[0] - byteRange[1]))
    return data

def main():
    bootSector = BootSector(getBytes([0x0, 0x48]))
    print(bootSector.info())


if __name__ == '__main__':
    main()
