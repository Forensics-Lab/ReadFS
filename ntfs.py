#!/usr/bin/python3

class NTFS:
    def __init__(self, reader, offset=0):
        self.reader = reader
        self.offset = offset

    def jump_instr(self):
        return self.reader.read_bytes(0, 2, offset=self.offset, bformat="hex")

    def OME_ID(self):
        return ''.join([chr(i) for i in self.reader.read_bytes(3, 10, offset=self.offset)]).strip()

    def BPS(self):
        return self.reader.read_bytes(11, 12, offset=self.offset, bformat="dec")

    def sec_per_cluster(self):
        return self.reader.read_bytes(13, 13, offset=self.offset, bformat="dec")

    def reserved(self):
        return self.reader.read_bytes(14, 15, offset=self.offset, bformat="hex")

    def unused(self):
        u1 = self.reader.read_bytes(19, 20, offset=self.offset, bformat="dec")
        u2 = self.reader.read_bytes(32, 39, offset=self.offset, bformat="dec")
        return hex(u1+u2)

    def media_desc(self):
        return self.reader.read_bytes(21, 21, offset=self.offset, bformat="hex")

    def sec_per_track(self):
        return self.reader.read_bytes(24, 25, offset=self.offset, bformat="dec")

    def heads_number(self):
        return self.reader.read_bytes(26, 27, offset=self.offset, bformat="dec")

    def hidden_secotrs(self):
        return self.reader.read_bytes(28, 31, offset=self.offset, bformat="dec")

    def total_secotrs(self):
        return self.reader.read_bytes(40, 47, offset=self.offset, bformat="dec")

    def logical_mft_cl(self):
        # Logical_mtf_cluster * sector_per_cluster * bytes_per_sector + offset
        return hex(self.reader.read_bytes(48, 55, offset=self.offset, bformat="dec") * self.sec_per_cluster() * self.BPS() + self.offset)

    def logical_mftmirr_cl(self):
        # Logical_mtfirr_cluster * sector_per_cluster * bytes_per_sector + offset
        return hex(self.reader.read_bytes(56, 63, offset=self.offset, bformat="dec") * self.sec_per_cluster() * self.BPS() + self.offset)

    def cl_per_file_rec_seg(self):
        return self.reader.read_bytes(64, 67, offset=self.offset, bformat="dec")

    def cl_per_index_block(self):
        return self.reader.read_bytes(68, 71, offset=self.offset, bformat="dec")

    def volume_serial_number(self):
        return self.reader.read_bytes(72, 79, offset=self.offset, bformat="hex")[2:].upper()

    def checksum(self):
        return self.reader.read_bytes(80, 82, offset=self.offset, bformat="hex")

    def get_all_attr(self):
        return self.jump_instr(), self.OME_ID(), self.BPS(), self.sec_per_cluster(), self.reserved(),\
            self.unused(), self.media_desc(), self.sec_per_track(), self.heads_number(), self.hidden_secotrs(),\
            self.total_secotrs(), self.logical_mft_cl(), self.logical_mftmirr_cl(), self.cl_per_file_rec_seg(),\
            self.cl_per_index_block(), self.volume_serial_number(), self.checksum()
