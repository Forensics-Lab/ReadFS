from typing import Union
from ReFS.bootsector import BootSector
from ReFS.superblock import Superblock
from ReFS.checkpoint import Checkpoint

def getBytes(byteRange: Union[list[bytes, int], tuple[bytes, int], set[bytes, int]], offset: Union[int, bytes] = 0) -> bytes:
    path = "samples/logical_refs_4Kb.001"
    with open(path, "rb") as file:
        file.seek(offset+ byteRange[0])
        data = file.read(abs(byteRange[0] - byteRange[1]))
    return data

def main():
    bootSector = BootSector(getBytes([0x0, 0x48]))
    pageSize = bootSector.sectorsPerCluster() * bootSector.bytesPerSector()
    sbo = bootSector.superBlockOffset()
    sb = Superblock(getBytes([0x0, pageSize], sbo))
    chkoff = sb.checkpointOffset()[0]
    checkpoint = Checkpoint(getBytes([0x0, pageSize], chkoff))

    # Uncomment line 21 to get information about ReFS's bootsector based on your logical forensic image 
    # print(bootSector.info())
    
    # Uncomment line 24 to get information about ReFS's superblock based on your logical forensic image
    # print(sb.info())
    
    # Uncomment line 28 to get information about ReFS's checkpoint based on your logical forensic image
    # print(checkpoint.info())

if __name__ == '__main__':
    main()
