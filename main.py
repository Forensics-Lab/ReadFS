import argparse
from ReFS.node import Node
from ReFS.bootsector import BootSector
from ReFS.superblock import Superblock
from ReFS.checkpoint import Checkpoint

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", help = "Path to file.", metavar='', required=True)
parser.add_argument("-ii", "--image_info", help = "Displays information about the partition found in the Boot Sector.", action="store_true")
parser.add_argument("-bi", "--block_info", help = "Retries separate bytes.", metavar='', choices=["superblock", "checkpoint"])
parser.add_argument("--node", help = "Specifie the offset to a node", metavar='', type=int)
parser.add_argument("--info", help = "Prints out data about the node (--node flag must be set)", action="store_true")
parser.add_argument("--entry", help = "Prints out data of a single entrie (--node flag must be set)", metavar='', type=int)
parser.add_argument("--entries", help = "Prints out data about all entries from a Node (--node flag must be set)", action="store_true")
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
    if args.node:
        node = Node(args.file, [0x0, clusterSize], args.node)
        if args.info:
            print(node.info())
        if args.entries:
            for entry in node.indexEntries().getEntries():
                print(entry)
        if args.entry:
            print(node.indexEntries().getEntries()[args.entry])

if __name__ == '__main__':
    main()
