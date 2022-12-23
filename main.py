from typing import Union
from ReFS.node import Node
from ReFS.bootsector import BootSector
from ReFS.superblock import Superblock
from ReFS.checkpoint import Checkpoint
from bytesFormater.formater import Formater

def getBytes(byteRange: Union[list[bytes, int], tuple[bytes, int], set[bytes, int]], offset: Union[int, bytes] = 0) -> bytes:
    path = "samples/logical_refs_64KB.001"
    with open(path, "rb") as file:
        file.seek(offset + byteRange[0])
        data = file.read(abs(byteRange[0] - byteRange[1]))
    return data

def main():
    formater = Formater()
    bootSector = BootSector(getBytes([0x0, 0x48]))
    clusterSize = bootSector.clusterSize()
    sbo = bootSector.superBlockOffset()
    sb = Superblock(getBytes([0x0, clusterSize], sbo))
    chkoff = sb.checkpointOffset()[0]
    checkpoint = Checkpoint(getBytes([0x0, clusterSize], chkoff))
    containerTablePointer = checkpoint.containerTablePointer() * clusterSize
    node = Node(getBytes([0x0, clusterSize], containerTablePointer))
    
    print(bootSector.info())
    print(sb.info())
    print(checkpoint.info())
    print(node.info())

if __name__ == '__main__':
    main()
