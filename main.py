import argparse
from ReFS.node import Node
from ReFS.bootsector import BootSector
from ReFS.superblock import Superblock
from ReFS.checkpoint import Checkpoint

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", help="Path to file", metavar='', required=True)

infoArgs = parser.add_argument_group("Info flags").add_mutually_exclusive_group()
infoArgs.add_argument("-ii", "--image_info", help="Displays information about the partition found in the Bootsector", action="store_true")
infoArgs.add_argument("-bi", "--block_info", help="Carves out data about either Superblock or Checkpoint", metavar='', choices=["superblock", "checkpoint"])
infoArgs.add_argument("-n", "--node", help="Specify the offset to a node", metavar='', type=int)

nodeArgs = parser.add_argument_group("Node required flags").add_mutually_exclusive_group()
nodeArgs.add_argument('--info', help='Prints out data about the node', action='store_true')
nodeArgs.add_argument('--entry', help='Prints out data of a single entry', metavar='', type=int)
nodeArgs.add_argument('--entries', help='Prints out data about all entries from a Node', action='store_true')

infoArgs.required = True if not parser.parse_args().node else False
nodeArgs.required = True if parser.parse_args().node else False

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

if __name__ == "__main__":
    main()