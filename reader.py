#!/usr/bin/python3

class Reader:
    def __init__(self, path):
        self.path = path

    def read_bytes(self, start, end, offset=0, bformat="bstr", order="little"):
        with open(self.path, "rb") as file:
            file.seek(start+offset)
            self.data = file.read(end-start+1)
        # Here I'd eventually just create a function to return me the data as a certain bytes format
        # Like string, decimal, hex, byte string and the little/big endians ordering.
        # it will look smthing like this
        # return self.format_bytes(self.data, bformat=bformat, order=order)
        return self.data

