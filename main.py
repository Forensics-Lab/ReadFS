from typing import Union
from ReFS.node import Node
from ReFS.bootsector import BootSector
from ReFS.superblock import Superblock
from ReFS.checkpoint import Checkpoint
from bytesFormater.formater import Formater

def getBytes(byteRange: Union[list[bytes, int], tuple[bytes, int], set[bytes, int]], offset: Union[int, bytes] = 0) -> bytes:
    path = "samples/logical_refs_64KB_3folders.001"
    # path = "samples/logical_refs_64KB.001"
    # path = "samples/logical_refs_4KB.001"
    with open(path, "rb") as file:
        file.seek(offset + byteRange[0])
        data = file.read(abs(byteRange[0] - byteRange[1]))
    return data

def main():
    formater = Formater()
    bootSector = BootSector(getBytes([0x0, 0x48]))
    pageSize = bootSector.sectorsPerCluster() * bootSector.bytesPerSector()
    sbo = bootSector.superBlockOffset()
    sb = Superblock(getBytes([0x0, pageSize], sbo))
    chkoff = sb.checkpointOffset()[0]
    checkpoint = Checkpoint(getBytes([0x0, pageSize], chkoff))
    containerTablePointer = checkpoint.containerTablePointer()
    offset = formater.toDecimal(checkpoint.byteArray[containerTablePointer:containerTablePointer+104][:4]) * pageSize
    node = Node(getBytes([0x0, pageSize], offset))
    

    print(bootSector.info())
    print(sb.info())
    print(checkpoint.info())
    print(node.info())

if __name__ == '__main__':
    main()
