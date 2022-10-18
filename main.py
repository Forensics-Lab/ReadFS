#!/usr/bin/python3
import argparse
from mbr import MBR
from ntfs import NTFS
from reader import Reader


parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", help = "Path to file", metavar='', required=True)
parser.add_argument("-p", "--partition", help = "Allows you to select a partition. This option should be used with a physical image", metavar='', type=int, choices=[1, 2, 3, 4], default=1)
parser.add_argument("-sp", "--show_partitions", help = "Shows all partitions from disk. Works only for physical images", action='store_true', default=None)
parser.add_argument("-ent", "--entry", help = "Allows to select an entry from NTFS", metavar='', choices=["boot"], default=None)
args = parser.parse_args()
 

reader = Reader(args.file)
mbr = MBR(reader)
ntfs = NTFS(reader)

partitions = mbr.get_all_partitions()
offset = 0 if NTFS(reader).OME_ID() == "NTFS" else partitions[args.partition-1].LBA()

if offset != 0 and args.show_partitions:
	for i in partitions:
		print(i.get_all_attr())
elif offset == 0 and args.show_partitions:
	print("[-] '-sp' flag can only be used on physical forensic images.")
	exit()

if args.entry == "boot":
	ntfs = NTFS(reader, offset=offset)
	print(ntfs.get_all_attr())


# I need to find a much more "elegant" way to parse those flags
# You can ran the script like so:

# python3 main.py -f samples/lo.001 -ent boot

# lo.001 is a logical forensic image. The -ent flag specifies the entry that the Reader class should read.
# For now the only supported entry is the Boot sector of the NTFS

# You can use the tool on physical forensic images as well like so:
# python3 main.py -f samples/ph.001 -sp
# The -sp flag allows you to view the partitions defined in the Master Boot Record image. This flag works only with physical forensic images

# If you are dealing with a physical image with a MBR that has more than one partitions defined on disk you can select the partition like so:
# python3 main.py -f samples/ph.001 -p 1
# the MBR can hold up to 4 partitions on disk so you will be able to pass only the numbers between 1 - 4 as a value for -p
