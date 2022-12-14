from json5 import load
from typing import Union
from struct import unpack


def getBytes(byteRange: Union[list[bytes, int], tuple[bytes, int], set[bytes, int]], offset: Union[int, bytes] = 0) -> bytes:
    path = "D:\\Uni\\Third Year\\CTS3510 Memory Analysis\\samples\\testingAlone\\refs_lo.001"
    with open(path, "rb") as file:
        file.seek(offset+ byteRange[0])
        data = file.read(abs(byteRange[0] - byteRange[1]))
    return data


def getFile(filePath:str, mode:str = "r") -> dict:
    with open(filePath, mode) as file:
        data = load(file)
    return data


def toDecimal(_bytes: bytes, order: str = "<", size="I") -> int:
    return unpack(f"{order}{size}", _bytes)[0]


def main():
    REFS_Offsets = getFile("REFS_offsets.json5")
    REFS_Boot_Sector = REFS_Offsets["bootSector"]
    print("<<=====================Boot Sector=====================>>\n"
          f"[+] Volume Boot Sector Size: {toDecimal(getBytes(REFS_Boot_Sector['sizeOfVBR']), size='h')} bytes\n"
          f"[+] Sectors per Cluster: {toDecimal(getBytes(REFS_Boot_Sector['sectorsPerCluster']))}\n"
          f"[+] Bytes per Sector: {toDecimal(getBytes(REFS_Boot_Sector['bytesPerSector']))}\n"
          f"[+] Number of Sectors: {toDecimal(getBytes(REFS_Boot_Sector['sectorCount']), size='q'):,}\n"
          f"[+] Volume size: {toDecimal(getBytes(REFS_Boot_Sector['sectorCount']), size='q') * toDecimal(getBytes(REFS_Boot_Sector['bytesPerSector'])):,} bytes\n"
          f"[+] Page size: {toDecimal(getBytes(REFS_Boot_Sector['bytesPerContainer']), size='q'):,} bytes\n"
          f"[+] Volume Serial Number: {getBytes(REFS_Boot_Sector['volumeSerialNumber'])[::-1].hex().upper()}\n"
          "<<=====================================================>>\n")


if __name__ == '__main__':
    main()
