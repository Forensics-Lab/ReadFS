from json5 import load
from typing import Union
from struct import pack, unpack


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


def toDecimal(_bytes: bytes, order: str = "<") -> int:
    return unpack(f"{order}I", _bytes)[0]


def superBlock(SectorsPerCluster:bytes, BytesPerSector:bytes) -> int:
    return 0x1e * toDecimal(SectorsPerCluster) * toDecimal(BytesPerSector)

def main():
    REFS_Offsets = getFile("D:\\Uni\\Third Year\\CST3590 Individual Project\\fsread\\REFS_offsets.json5")
    REFS_Boot_Sector = REFS_Offsets["bootSector"]
    REFS_Page_Header = REFS_Offsets["pageHeader"]


    spc = getBytes(REFS_Boot_Sector["sectorsPerCluster"])
    bps = getBytes(REFS_Boot_Sector["bytesPerSector"])
    
    superBlockOffset = superBlock(spc, bps)
    pageSig = getBytes(REFS_Page_Header["pageSignature"], superBlockOffset)
    print(pageSig)

if __name__ == '__main__':
    main()
