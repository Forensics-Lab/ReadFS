#!/usr/bin/python3
import argparse
from fileSystems import *
from bootSectorReaders import *


parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", help = "Path to file", metavar='', required=True)
parser.add_argument("-it", "--img_type", help = "Forensic image type. Logical or Physical (lo - ph)", metavar='', required=True)
parser.add_argument("-fs", "--fs_type", help = "Specify the file system type", metavar='', default="ntfs")
parser.add_argument("-gb", "--grab", help = "Retries separate bytes.", metavar='', default=True)
parser.add_argument("-pt", "--partition", help = "Allows you to select the partition to inspect if dealing with a physical image", metavar='', type=int, default=0)
args = parser.parse_args()


fs_types = ["ntfs", "fat", "xfat", "fat16", "fat32"]
img_types = ["lo", "ph", "logical", "physical"]


if args.fs_type.lower() not in fs_types:
	parser.error(f"Unknown file system type. Supported types: {fs_types}")

if args.img_type not in img_types:
	parser.error(f"Unknown forensic image format. Supported formats: {img_types}")

reader = Reader(args.file)

if args.img_type == "physical" or args.img_type == "ph":
	if args.fs_type == "NTFS" or args.fs_type == "ntfs":
		# Getting all NTFS partitions and defaulting 
		partition = reader.get_partitions_of_type("0x7", MBR().get_partitions())[args.partition]
		start2, end2, bformat2 = MBR().get_offsets("LBA")
		LBA = reader.get_bytes(start2+partition[0], end2+partition[0], bformat=bformat2)
		offset = LBA*512
		y = bootSector().get_all()
		
		# Outputting partition essential bytes
		for i in y:
			start, end, bformat = i.values()
			x = reader.get_bytes(start, end, bformat=bformat, offset=offset)
			print(x)

elif args.img_type == "logical" or args.img_type == "lo":
	if args.fs_type == "NTFS" or args.fs_type == "ntfs":
		start1, end1, bformat1 = bootSector().get_offsets("logical_mft_cluster")
		start2, end2, bformat2 = bootSector().get_offsets("sec_per_cluster")
		start3, end3, bformat3 = bootSector().get_offsets("BPS")

		lo_mft_cl = reader.get_bytes(start1, end1, bformat=bformat1)
		sc_per_cl = reader.get_bytes(start2, end2, bformat=bformat2)
		bps = reader.get_bytes(start3, end3, bformat=bformat3)

		offset = lo_mft_cl * sc_per_cl * bps
		y = MFTEntrie().get_all()
		for i in y:
			start, end, bformat = i.values()
			x = reader.get_bytes(start, end, bformat=bformat, offset=offset)
			print(x)