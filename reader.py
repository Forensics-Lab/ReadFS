#!/usr/bin/python3

class Reader:
	def __init__(self, path):
		self.path = path

	def read_bytes(self, start, end, offset=0, bformat="bstr", order="little"):
		with open(self.path, "rb") as file:
			file.seek(start+offset)
			self.data = file.read(end-start+1)
		return self.data

