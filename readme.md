# About the project
This idea started after I choose my university final year project and I learned that Microsoft has developed a new file system that removes some limitations that NTFS has and deals better with data corruption. After looking around to see if there are any tools or pieces of software 

The project is aiming to fit the needs of a day-to-day user and help out in data loss recovery, also I want to build a robust, powerful, and easy-to-use framework for forensic applications in which the logical/physical forensic image is formatted with ReFS.

# Giving credit where credit is due
This project wouldn't be possible or would be really hard to accomplish without the help of a paper written by Paul Prade, Tobias Groß, Andreas Dewald from Friedrich Alexander University
Erlangen-Nuremberg. Please feel free to go and read their amazing paper here -> https://doi.org/10.25593/issn.2191-5008/CS-2019-05

# Current capabilities
- The ability to correctly parse and output information from the following:
    - Boot sector
    - Superblock
    - Checkpoint
    - Nodes

# Usage
To display general information about the forensic image you will need to pass the -ii or --image_info flags. See the example bellow:
```cmd
$> py main.py -f path/to/file.001 -ii

<<=====================[Boot Sector]=====================>>
[+] ReFS Version: 3.4
[+] Super Block Offset: 1966080 bytes
[+] VBR Size: 512 bytes
[+] Bytes per Sector: 512
[+] Cluster size: 65,536 bytes
[+] Sectors per Cluster: 128
[+] Clusters per Container: 1,024
[+] Number of Containers: 79
[+] Number of Clusters: 80,896
[+] Number of Sectors: 10,354,688
[+] Container size: 67,108,864 bytes
[+] Volume size: 5,301,600,256 bytes
[+] Volume Serial Number: 7EBA2960BA2915E5
<<=======================================================>>
```

At this stage in development the tool is able to parse the data found in the Superblock, Checkpoint and individual Table Nodes but I didn't implement a flag that allows you to view data by passing a offset to a node yet. 
As I said, in the mean time, please use the bellow command to get the information stored in the Superblock:

```cmd
$> py main.py -f path/to/file.001 -bi superblock

<<=====================[Page Header]=====================>>
[+] Page Signature: SUPB
[+] Volume Signature: 5C1FB1E2
[+] LCN_0: 30
[+] LCN_1: 0
[+] LCN_2: 0
[+] LCN_3: 0
[+] Table Type: Not A Table
<<======================[Superblock]=====================>>
[+] GUID: 5C1FB1E2
[+] Superblock Version: 1
[+] Checkpoint Reference Number: 2
[+] Checkpoint1 Offset: 55312384 bytes
[+] Checkpoint2 Offset: 638255104 bytes
[+] Self Descriptor Relative Offset: 208 bytes
[+] Self Descriptor Length: 104 bytes
<<================[Self Page Descriptor]=================>>
[+] LCN_0: 30
[+] LCN_1: 0
[+] LCN_2: 0
[+] LCN_3: 0
[+] Checksum Type: CRC64-ECMA-182
[+] Checksum Offset: 8
[+] Checksum Length: 8
<<=================[Page Data Checksum]==================>>
[+] Page Data Checksum: DDA05B730320F31C
<<=======================================================>>
```
You can do the exact same thing with the Checkpoint:
```cmd
$> py main.py -f path/to/file.001 -bi superblock

<<=====================[Page Header]=====================>>
[+] Page Signature: CHKP
[+] Volume Signature: 5C1FB1E2
[+] LCN_0: 844
[+] LCN_1: 0
[+] LCN_2: 0
[+] LCN_3: 0
[+] Table Type: Not A Table
<<======================[Checkpoint]=====================>>
[+] ReFS Version: 3.4
[+] Self Descriptor Relative Offset: 208
[+] Self Descriptor Length: 104
[+] Checkpoint Virtual Clock: 17
[+] Allocator Virtual Clock: 13
[+] Oldest Log Record: 2
[+] Reserved: 0
<<============[Pointers Cluster Offset Info]=============>>
[+] Count: 13
[+] Object ID Table: 4618
[+] Duplicate Object ID Table: 4619
[+] Medium Allocator Table: 29187
[+] Container Allocator Table: 28673
[+] Schema Table: 4141
[+] Duplicate Schema Table: 4142
[+] Parent Child Table: 4620
[+] Block Reference Count Table: 28675
[+] Container Table: 1027
[+] Duplicate Container Table: 1028
[+] Container Index Table: 4137
[+] Integrity State Table: 28674
[+] Small Allocator Table: 1030
<<================[Self Page Descriptor]=================>>
[+] LCN_0: 844
[+] LCN_1: 0
[+] LCN_2: 0
[+] LCN_3: 0
[+] Checksum Type: CRC64-ECMA-182
[+] Checksum Offset: 8
[+] Checksum Length: 8
<<=================[Page Data Checksum]==================>>
[+] Page Data Checksum: 4FE421E97BEC00C5
<<=======================================================>>
```
## !! IMPORTANT !!!
I am in the process of implementing the algorithm that translates virtual-to-physical addresses used by ReFS. With that said the only usable offset from the pointers section is the Container Table and the Duplicate Container Table because they hold  the needed information for this process. 

# What's next?
- Implementing the algorithm needed to translate virtual addresses to physical ones.
- Correctly displaying the offsets of all the tables in the file system.
- Adding support for the rest of the tables in the file system.
- Implementing ways to view the files/folders present in the forensic image. (Deleted or not)
- Adding the ability to recover deleted or non-deleted files/folders from the forensic image.