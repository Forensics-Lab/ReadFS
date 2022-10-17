#!/usr/bin/python3
import argparse
from mbr import MBR
from ntfs import NTFS
from reader import Reader


parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", help = "Path to file", metavar='', required=True)
parser.add_argument("-it", "--img_type", help = "Forensic image type. Logical or Physical (lo - ph)", metavar='', required=False)
parser.add_argument("-fs", "--fs_type", help = "Specify the file system type", metavar='', default="ntfs")
parser.add_argument("-gb", "--grab", help = "Retries separate bytes.", metavar='', default=True)
parser.add_argument("-pt", "--partition", help = "Allows you to select the partition to inspect if dealing with a physical image", metavar='', type=int, default=0)
args = parser.parse_args()

reader = Reader(args.file)
mbr = MBR(reader)

partitions = mbr.get_all_partitions()
for i in partitions:
	print(i.get_all_attr())

ntfs = NTFS(reader, offset=partitions[0].LBA())
print(ntfs.BPS())

# print(ntfs.logical_mft_cl())
