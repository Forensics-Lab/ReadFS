import argparse
from ReFS.bootsector import BootSector
from ReFS.superblock import Superblock
from ReFS.checkpoint import Checkpoint

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", help = "Path to file.", metavar='', required=True)
parser.add_argument("-ii", "--image_info", help = "Displays information about the partition found in the Boot Sector.", action="store_true")
parser.add_argument("-bi", "--block_info", help = "Retries separate bytes.", metavar='', choices=["superblock", "checkpoint"])
args = parser.parse_args()


def main():
    bootSector = BootSector(args.file, [0x0, 0x48])
    clusterSize = bootSector.clusterSize()
    superblockOffset = bootSector.superBlockOffset()
    superblock = Superblock(args.file, [0x0, clusterSize], superblockOffset)
    checkpointOffset = superblock.checkpointOffset()[0]
    checkpoint = Checkpoint(args.file, [0x0, clusterSize], checkpointOffset)

    if args.image_info:
        print(bootSector.info())
    if args.block_info:
        if args.block_info == "superblock":        
            print(superblock.info())
        elif args.block_info == "checkpoint":
            print(checkpoint.info())

if __name__ == '__main__':
    main()
