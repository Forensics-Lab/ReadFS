from typing import Union
from bytesFormater.formater import Formater

class BootSector():
    def __init__(self, byteArray:Union[list[bytes], tuple[bytes], set[bytes]]) -> None:
        self.byteArray = byteArray
        self.formater = Formater()

    def assemblyCode(self) -> str:
        return self.formater.toHex(self.byteArray[0x0:0x03])

    def REFSSifniture(self) -> str:
        return self.formater.toString(self.byteArray[0x03:0x0B])

    def mustBeZero(self) -> int:
        return self.formater.toDecimal(self.byteArray[0x0B:0x10])

    def FSRSIdentifier(self) -> str:
        return self.formater.toString(self.byteArray[0x10:0x14])

    def sizeOfVBR(self) -> int:
        return self.formater.toDecimal(self.byteArray[0x14:0x16])

    def checksum(self) -> str:
        return self.formater.toHex(self.byteArray[0x16:0x18])

    def sectorCount(self) -> int:
        return self.formater.toDecimal(self.byteArray[0x18:0x20])

    def bytesPerSector(self) -> int:
        return self.formater.toDecimal(self.byteArray[0x20:0x24])

    def sectorsPerCluster(self) -> int:
        return self.formater.toDecimal(self.byteArray[0x24:0x28])

    def ReFSVersion(self) -> str:
        major, minor = self.byteArray[0x28:0x2A]
        return f"{major}.{minor}"

    def volumeSerialNumber(self) -> str:
        return self.formater.toHex(self.byteArray[0x38:0x40])

    def bytesPerContainer(self) -> int:
        return self.formater.toDecimal(self.byteArray[0x40:0x48])

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
              f"<<=======================================================>>\n"
