from struct import unpack
from Managers.Bytes import Formater


''' https://learn.microsoft.com/windows/win32/fileio/computing-a-file-system-recognition-checksum '''
class FSChecksum():
    def __init__(self, data: bytes):
        self._checksum = 0
        for value in data:
            self._checksum = (0x8000 if (self._checksum & 1) else 0) \
            + (self._checksum >> 1) + value

    def checksum(self): return self._checksum.to_bytes(length=2, byteorder='little')


class BootSector():
    def __init__(self, _bytes: bytes) -> None:
        self.formater = Formater()
        self.bStruct = unpack("<3s8s5s4sh2sq2i2b6s8s8sq", _bytes[:0x48])
        self.chksum = self.formater.toHex(FSChecksum(_bytes[3:22] + _bytes[24:]).checksum())

    def assemblyCode(self) -> str:
        return self.bStruct[0]

    def REFSSifniture(self) -> str:
        return self.formater.toString(self.bStruct[1])

    def mustBeZero(self) -> int:
        return self.bStruct[2]

    def FSRSIdentifier(self) -> str:
        return self.formater.toString(self.bStruct[3])

    def sizeOfVBR(self) -> int:
        return self.bStruct[4]

    def checksum(self) -> str:
        return self.formater.toHex(self.bStruct[5])

    def sectorCount(self) -> int:
        return self.bStruct[6]

    def bytesPerSector(self) -> int:
        return self.bStruct[7]

    def sectorsPerCluster(self) -> int:
        return self.bStruct[8]

    def ReFSVersion(self) -> str:
        return f"{self.bStruct[9]}.{self.bStruct[10]}"

    def volumeSerialNumber(self) -> str:
        return self.formater.toHex(self.bStruct[13])

    def bytesPerContainer(self) -> int:
        return self.bStruct[14]

    def superBlockOffset(self) -> int:
        return 0x1e * self.sectorsPerCluster() * self.bytesPerSector()

    def clusterSize(self) -> int:
        return self.sectorsPerCluster() * self.bytesPerSector()
    
    def numberOfContainers(self) -> int:
        return (self.bytesPerSector() * self.sectorCount()) // self.bytesPerContainer()

    def numberOfClusters(self) -> int:
        return self.sectorCount() // self.sectorsPerCluster()

    def numberOfClustersPerContainer(self) -> int:
        return self.numberOfClusters() // self.numberOfContainers()

    def info(self) -> str:
        return "<<=====================[Boot Sector]=====================>>\n"\
              f"[+] ReFS Version: {self.ReFSVersion()}\n"\
              f"[+] Super Block Offset: {self.superBlockOffset()} bytes\n"\
              f"[+] VBR Size: {self.sizeOfVBR()} bytes\n"\
              f"[+] Bytes per Sector: {self.bytesPerSector()}\n"\
              f"[+] Cluster size: {self.clusterSize():,} bytes\n"\
              f"[+] Sectors per Cluster: {self.sectorsPerCluster()}\n"\
              f"[+] Clusters per Container: {self.numberOfClustersPerContainer():,}\n"\
              f"[+] Number of Containers: {self.numberOfContainers()}\n"\
              f"[+] Number of Clusters: {self.numberOfClusters():,}\n"\
              f"[+] Number of Sectors: {self.sectorCount():,}\n"\
              f"[+] Container size: {self.bytesPerContainer():,} bytes\n"\
              f"[+] Volume size: {self.bytesPerSector() * self.sectorCount():,} bytes\n"\
              f"[+] Volume Serial Number: {self.volumeSerialNumber()}\n"\
              f"[+] File System Checksum: {self.checksum()} ({self.chksum == self.checksum()})\n"\
              f"<<=======================================================>>"
