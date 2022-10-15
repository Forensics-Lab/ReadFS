class Reader:
	def __init__(self, path):
		self.path = path

	def get_bytes(self, start, end, offset=0, bformat="bstr", order="little"):
		with open(self.path, "rb") as file:
			file.seek(start+offset)
			data = file.read(end-start+1)
		return self.format_bytes(data, bformat, order)

	def format_bytes(self, _bytes, bformat=None, order="little"):
		if bformat == "hex":
			return hex(int.from_bytes(_bytes, order))
		elif bformat == "dec":
			return int.from_bytes(_bytes, order)
		elif bformat == "str":
			return ''.join([chr(i) for i in _bytes])
		elif bformat == "bstr":
			return _bytes

	def get_partitions_of_type(self, type, partitions):
		tmp = []
		for partition in partitions:
			start, end, bformat = list(partition)[0], list(partition)[1], list(partition)[2], 
			p_type = self.get_bytes(start, end, bformat=bformat)[4]
			if hex(p_type) == "0x7":
				tmp.append(list(partition))
		return tmp