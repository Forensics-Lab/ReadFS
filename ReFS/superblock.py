from ReFS.pageHeader import PageHeader
from bytesFormater.formater import Formater

class Superblock:
    def __init__(self, byteArray, bootsector) -> None:
        self.byteArray = byteArray
        self.pageHeader = PageHeader(self.byteArray[0x0:0x50])
        self.formater = Formater()
        self.bootsector = bootsector

    def GUID(self) -> str:
        temp = [self.formater.toDecimal(self.byteArray[0x50:0x60][i:i+4]) for i in range(0, len(self.byteArray[0x50:0x60]), 4)]
        sig = hex(temp[0] ^ temp[1] ^ temp[2] ^ temp[3])[2:]
        return ' '.join([sig[i:i+2] for i in range(0, len(sig), 2)]).upper()
    
    def version(self) -> int:
        return self.formater.toDecimal(self.byteArray[0x68:0x70])

    def checkpointOffset(self) -> tuple[int, int]:
        byteArrayRelativeOffset = self.formater.toDecimal(self.byteArray[0x70:0x74]) % len(self.byteArray)
        bytesPerCluster = self.bootsector.sectorsPerCluster() * self.bootsector.bytesPerSector()
        chk1 = self.formater.toDecimal(self.byteArray[byteArrayRelativeOffset:byteArrayRelativeOffset+0x08]) * bytesPerCluster 
        chk2 = self.formater.toDecimal(self.byteArray[byteArrayRelativeOffset+0x08:byteArrayRelativeOffset+0x10]) * bytesPerCluster
        return  chk1, chk2

    def checkpointReferenceNumber(self) -> int:
        return self.formater.toDecimal(self.byteArray[0x74:0x78])

    def selfDescriptorOffset(self) -> int:
        return self.formater.toDecimal(self.byteArray[0x78:0x7C])

    def selfDescriptorLength(self) -> int:
        return self.formater.toDecimal(self.byteArray[0x7C:0x80])

    def info(self) -> str:
        checkpoint1, checkpoint2 = self.checkpointOffset()
        return f"{self.pageHeader.info()}\n"\
               f"<<======================Superblock=====================>>\n"\
               f"[+] GUID: {self.GUID()}\n"\
               f"[+] Superblock Version: {self.version()}\n"\
               f"[+] Checkpoint Reference Number: {self.checkpointReferenceNumber()}\n"\
               f"[+] Checkpoint1 Offset: {checkpoint1} bytes\n"\
               f"[+] Checkpoint2 Offset: {checkpoint2} bytes\n"\
               f"[+] Self Descriptor Offset: {self.selfDescriptorOffset()} bytes\n"\
               f"[+] Self Descriptor Length: {self.selfDescriptorLength()} bytes\n"\
               f"<<=====================================================>>\n"\
