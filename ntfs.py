#!/usr/bin/python3

class NTFS:
	def __init__(self, reader, offset=0):
		self.reader = reader
		self.offset = offset

	def jump_instr(self):
		return self.reader.read_bytes(0, 2, offset=self.offset)

	def OME_ID(self):
		return self.reader.read_bytes(3, 10, offset=self.offset).decode("utf-8").strip()

	def BPS(self):
		return int.from_bytes(self.reader.read_bytes(11, 12, offset=self.offset), "little")

	def sec_per_cluster(self):
		return int.from_bytes(self.reader.read_bytes(13, 13, offset=self.offset), "little")

	def reserved(self):
		return hex(int.from_bytes(self.reader.read_bytes(14, 15, offset=self.offset), "little"))

	def unused(self):
		u1 = int.from_bytes(self.reader.read_bytes(19, 20, offset=self.offset), "little")
		u2 = int.from_bytes(self.reader.read_bytes(32, 39, offset=self.offset), "little")
		return hex(u1+u2)

	def media_desc(self):
		return hex(int.from_bytes(self.reader.read_bytes(21, 21, offset=self.offset), "little"))

	def sec_per_track(self):
		return int.from_bytes(self.reader.read_bytes(24, 25, offset=self.offset), "little")

	def heads_number(self):
		return int.from_bytes(self.reader.read_bytes(26, 27, offset=self.offset), "little")

	def hidden_secotrs(self):
		return int.from_bytes(self.reader.read_bytes(28, 31, offset=self.offset), "little")

	def total_secotrs(self):
		return int.from_bytes(self.reader.read_bytes(40, 47, offset=self.offset), "little")

	def logical_mft_cl(self):
		# Logical_mtf_cluster * sector_per_cluster * bytes_per_sector + offset
		return hex(int.from_bytes(self.reader.read_bytes(48, 55, offset=self.offset), "little") * self.sec_per_cluster() * self.BPS()+self.offset)

	def logical_mftmirr_cl(self):
		# Logical_mtfirr_cluster * sector_per_cluster * bytes_per_sector + offset
		return hex(int.from_bytes(self.reader.read_bytes(56, 63, offset=self.offset), "little")  * self.sec_per_cluster() * self.BPS()+self.offset)

	def cl_per_file_rec_seg(self):
		return int.from_bytes(self.reader.read_bytes(64, 67, offset=self.offset), "little")

	def cl_per_index_block(self):
		return int.from_bytes(self.reader.read_bytes(68, 71, offset=self.offset), "little")

	def volume_serial_number(self):
		return hex(int.from_bytes(self.reader.read_bytes(72, 79, offset=self.offset), "little"))[2:].upper()

	def checksum(self):
		return hex(int.from_bytes(self.reader.read_bytes(80, 82, offset=self.offset), "little"))









