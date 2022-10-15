#!/usr/bin/python3
import json

class bootSector():
	def __init__(self):
		with open("fileSystems/NTFS/NTFS_MASTER_BOOT_RECORD_BYTES.json", "r") as file:
			self.data = json.load(file)

	def get_offsets(self, attr):
		return self.data[attr].values()

	def get_all(self):
		return self.data.values()