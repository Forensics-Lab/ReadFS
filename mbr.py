#!/usr/bin/python3

class MBR:
    def __init__(self, reader):
        self.reader = reader

    def boot_code(self):
        return self.reader.read_bytes(0, 445)

    def p1(self):
        return Partition(self.reader.read_bytes(446, 461))

    def p2(self):
        return Partition(self.reader.read_bytes(462, 477))

    def p3(self):
        return Partition(self.reader.read_bytes(478, 493))

    def p4(self):
        return Partition(self.reader.read_bytes(494, 509))

    def get_all_partitions(self):
        return self.p1(), self.p2(), self.p3(), self.p4()


class Partition:
    def __init__(self, partition):
        self.partition = partition

    def boot_flag(self):
        return hex(self.partition[0])

    def CHS_start(self):
        return hex(int.from_bytes(self.partition[1:4], "little"))

    def p_type(self):
        return hex(self.partition[4])

    def CHS_end(self):
        return hex(int.from_bytes(self.partition[5:8], "little"))

    def LBA(self):
        return int.from_bytes(self.partition[8:12], "little")*512

    def size_in_sectors(self):
        return round(int.from_bytes(self.partition[12:16], "little")*512/1073741824, 2)

    def get_all_attr(self):
        return self.boot_flag(), self.CHS_start(), self.p_type(), self.CHS_end(),\
            hex(self.LBA()), self.size_in_sectors()
