#!/usr/bin/python3
import json

class MBR():

    def __init__(self):
        with open("bootSectorReaders/MBR_PARTITION_BYTES.json", "r") as file:
            self.data = json.load(file)

    def get_offsets(self, attr):
        return self.data[attr].values()

    def get_partitions(self):
        return self.data["p1"].values(), self.data["p2"].values(), self.data["p3"].values(), self.data["p4"].values()

    def get_all(self):
        return self.data.values()