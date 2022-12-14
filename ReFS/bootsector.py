from typing import Union
from bytesFormater.formater import Formater


class BootSector():
    def __init__(self, byteArray:Union[list[bytes], tuple[bytes], set[bytes]]) -> None:
        self.byteArray = byteArray
        self.formater = Formater()
    
    def assemblyCode(self):
        return self.formater.toHex(self.byteArray[0x0:0x03])
    
    def REFSSifniture(self):
        return self.formater.toString(self.byteArray[0x03:0x0B])
    
    def mustBeZero(self):
        return self.formater.toDecimal(self.byteArray[0x0B:0x10])

    def FSRSIdentifier(self):
        return self.formater.toString(self.byteArray[0x10:0x14])

    def sizeOfVBR(self):
        return self.formater.toDecimal(self.byteArray[0x14:0x16])
    
    def checksum(self):
        return self.formater.toHex(self.byteArray[0x16:0x18])
    
    def sectorCount(self):
        return self.formater.toDecimal(self.byteArray[0x18:0x20])
    
    def bytesPerSector(self):
        return self.formater.toDecimal(self.byteArray[0x20:0x24])
    
    def sectorsPerCluster(self):
        return self.formater.toDecimal(self.byteArray[0x24:0x28])
    
    def ReFSVersion(self):
        major, minor = self.byteArray[0x28:0x2A]
        return f"{major}.{minor}"
    
    def volumeSerialNumber(self):
        return self.formater.toHex(self.byteArray[0x38:0x40])
    
    def bytesPerContainer(self):
        return self.formater.toDecimal(self.byteArray[0x40:0x48])

    def info(self) -> str:
        return "<<=====================Boot Sector=====================>>\n"\
              f"[+] ReFS Version: {self.ReFSVersion()}\n"\
              f"[+] VBR Size: {self.sizeOfVBR()} bytes\n"\
              f"[+] Sectors per Cluster: {self.sectorsPerCluster()}\n"\
              f"[+] Bytes per Sector: {self.bytesPerSector()}\n"\
              f"[+] Number of Sectors: {self.sectorCount():,}\n"\
              f"[+] Volume size: {self.bytesPerSector() * self.sectorCount():,} bytes\n"\
              f"[+] Page size: {self.bytesPerContainer():,} bytes\n"\
              f"[+] Volume Serial Number: {self.volumeSerialNumber()}\n"\
              "<<=====================================================>>\n"