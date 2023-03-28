import argparse
from ReFS.Node import Node
from Managers.EvidenceFile import Reader
from ReFS.MainBlocks import BootSector, Superblock, Checkpoint

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

entriesArgs = parser.add_argument_group("Entries flags").add_mutually_exclusive_group()
entriesArgs.add_argument('--json', help='Prints out key:value information as a dictionary', action='store_true')
entriesArgs.add_argument('--table', help='Prints out key information in a table format', action='store_true')

infoArgs.required = True if not parser.parse_args().node else False
nodeArgs.required = True if parser.parse_args().node else False
entriesArgs.required = True if (parser.parse_args().entries or parser.parse_args().entry) else False

args = parser.parse_args()

def main():
    EVIDENCE_FILE = Reader(args.file)
    bootSector = BootSector(EVIDENCE_FILE.getBytes(0x48))
    superblock = Superblock(EVIDENCE_FILE.getBytes(bootSector.clusterSize(), bootSector.superBlockOffset()))
    checkpoint = Checkpoint(EVIDENCE_FILE.getBytes(bootSector.clusterSize(), superblock.checkpointOffset()[0]))
    checkpoint.setContainerTableEntries(Node(EVIDENCE_FILE.getBytes(bootSector.clusterSize(), checkpoint.containerTablePointer())).indexEntries().getEntries())

    if args.image_info:
        print(bootSector.info())
    if args.block_info == "superblock":
        print(superblock.info())
    if args.block_info == "checkpoint":
        print(checkpoint.info())
    if args.node:
        node = Node(EVIDENCE_FILE.getBytes(bootSector.clusterSize(), args.node))
        indexEntry = node.indexEntries()
        if args.info:
            print(node.info())
        if args.entries and args.json:
            for entry in indexEntry.getEntries():
                print(entry)
        if args.entries and args.table:
                print(indexEntry.logEntry())
        if args.entry and args.json:
            print(indexEntry.getEntries()[args.entry])
        if args.entry and args.table:
            print(indexEntry.logEntry(args.entry))

if __name__ == "__main__":
    main()