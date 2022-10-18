#!/usr/bin/python3
import argparse
from mbr import MBR
from ntfs import NTFS
from reader import Reader


parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", help = "Path to file", metavar='', required=True)
parser.add_argument("-fs", "--fs_type", help = "Specify the file system type", metavar='', default="ntfs")
parser.add_argument("-p", "--partition", help = "Allows you to select a partition. This option should be used with a phisical image", metavar='', type=int, choices=[1, 2, 3, 4], default=1)

# Will have to work on the -sp flag 
# parser.add_argument("-sp", "--show_partitions", help = "Shows all partitions from disk. Works only for phisical images", action='store_true')

args = parser.parse_args()

reader = Reader(args.file)
mbr = MBR(reader)
partitions = mbr.get_all_partitions()
offset = 0 if NTFS(reader).OME_ID() == "NTFS" else partitions[args.partition-1].LBA()

ntfs = NTFS(reader, offset=offset)
print(ntfs.get_all_attr())
