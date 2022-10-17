#!/usr/bin/python3
import argparse
from mbr import MBR
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

for partition in partitions:
	print(partition.get_all_attr())
