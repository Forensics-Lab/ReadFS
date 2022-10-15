#!/usr/bin/python3
import json

class MFTEntrie():
	def __init__(self):
		with open("fileSystems/NTFS/NTFS_ENTRIES_BYTES.json", "r") as file:
			self.data = json.load(file)

	def get(self, attr):
		return self.data[attr].values()

	def get_all(self):
		return self.data.values()