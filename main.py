import argparse
from typing import Union
from ReFS.node import Node
from ReFS.bootsector import BootSector
from ReFS.superblock import Superblock
from ReFS.checkpoint import Checkpoint
from bytesFormater.formater import Formater

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", help = "Path to file.", metavar='', required=True)
parser.add_argument("-ii", "--image_info", help = "Displays information about the partition found in the Boot Sector.", action="store_true")
parser.add_argument("-bi", "--block_info", help = "Retries separate bytes.", metavar='', choices=["superblock", "checkpoint"])
args = parser.parse_args()


def getBytes(file_path: str, byteRange: Union[list[bytes, int], tuple[bytes, int], set[bytes, int]], offset: Union[int, bytes] = 0) -> bytes:
    with open(file_path, "rb") as file:
        file.seek(offset + byteRange[0])
        data = file.read(abs(byteRange[0] - byteRange[1]))
    return data

def main():
    bootSector = BootSector(getBytes(args.file , [0x0, 0x48]))
    clusterSize = bootSector.clusterSize()
    superblockOffset = bootSector.superBlockOffset()
    superblock = Superblock(getBytes(args.file, [0x0, clusterSize], superblockOffset))
    primaryCheckpointOffset = superblock.checkpointOffset()[0]
    _backupCheckpointOffset = superblock.checkpointOffset()[1]
    _backupCheckpointContainerTableOffset = Checkpoint(getBytes(args.file, [0x0, clusterSize], _backupCheckpointOffset)).containerTablePointer() * clusterSize
    _containerTableNode = Node(getBytes(args.file, [0x0, clusterSize], _backupCheckpointContainerTableOffset))
    primaryCheckpoint = Checkpoint(getBytes(args.file, [0x0, clusterSize], primaryCheckpointOffset), _containerTableNode)

    if args.image_info:
        print(bootSector.info())
    if args.block_info:
        if args.block_info == "superblock":        
            print(superblock.info())
        elif args.block_info == "checkpoint":
            print(primaryCheckpoint.info())


if __name__ == '__main__':
    main()
