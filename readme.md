# About the project

This project started after I learned that Microsoft has developed a new file system that removes some limitations that NTFS has and deals better with data corruption. After looking around to see if there are any tools or pieces of software that can parse this type of file system I could only find 5 products which have support for ReFS but I think those tools can be improved. 

With that said, this project aims to fit the needs of a day-to-day user and help out with data loss recovery and forensics investigations. The plan is to build a console-based utility for windows or linux that will help forensic investigators parse ReFS foremated disks images created by FTK Imager.

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

## Bootsector
To display general information about the forensic image you will need to pass the -ii or --image_info flags. See the example bellow:
```cmd
$> py main.py -f path/to/file.001 -ii
```
```
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
## Superblock
The information stored in the Superblock structure can be extracted using the command bellow:

```cmd
$> py main.py -f path/to/file.001 -bi superblock
```
```
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
## Checkpoint
The information stored in the Checkpoint can be extracted using the command bellow:
```cmd
$> py main.py -f path/to/file.001 -bi checkpoint
```
```
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
<<=============[Pointers Bytes Offset Info]==============>>
[+] Object ID Table: 34209792
[+] Duplicate Object ID Table: 34275328
[+] Medium Allocator Table: 36896768
[+] Container Allocator Table: 3211264
[+] Schema Table: 2949120
[+] Duplicate Schema Table: 3014656
[+] Parent Child Table: 34340864
[+] Block Reference Count Table: 3342336
[+] Container Table: 67305472
[+] Duplicate Container Table: 67371008
[+] Container Index Table: 2686976
[+] Integrity State Table: 3276800
[+] Small Allocator Table: 67502080
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
## Node
As of now the only tables that the Node class can parse are the Container Table, Object ID and their duplicates, in the near future this will change!

General Node information can be displayed by passing the offset to a table found in the checkpoint. Let's take the Object ID Table pointer offset for example:
```cmd
$> py main.py -f path/to/file.001 --node 33751040 --info
```
```
<<=====================[Page Header]=====================>>
[+] Page Signature: MSB+
[+] Volume Signature: 5C1FB1E2
[+] LCN_0: 4611
[+] LCN_1: 0
[+] LCN_2: 0
[+] LCN_3: 0
[+] Table Type: Object ID
<<=================[Index Root Element]==================>>
[+] Size: 552
[+] Root Fixed Size: 40
[+] Table Schema 1 Identifier: E030
[+] Table Schema 2 Identifier: E030
[+] Table Rows Number: 18
[+] Number of Extents: 0
<<====================[Index Header]=====================>>
[+] Node Type: Root
[+] Node Height: 0
[+] Start Of Data Area: 40
[+] End Of Data Area: 5000
[+] Key Index Start: 64832
[+] Key Index End: 64904
[+] Key Index Entries: 18
[+] Node Free Bytes: 59832
<<=======================================================>>
```
Every table found in the Checkpoint Block has entries/rows in them, those can be extracted by using the --entries flag:
```cmd
$> py main.py -f path/to/file.001 --node 33751040 --entries
```
```
[...snip...]
{'Entry size': 272, 'Key Offset Start': 16, 'Key Size': 16, 'Flag': 'Not Set', 'Value Start Offset': 32, 'Value Size': 240, 'Object ID': {'ID': 'Upcase Table', 'Durable LSN Offset': 24, 'Buffer Offset': 200, 'Buffer Length': 0, 'Durable LSN': (0, 0), 'Page Reference': (4144, 0, 0, 0), 'Buffer Data': b''}}
{'Entry size': 272, 'Key Offset Start': 16, 'Key Size': 16, 'Flag': 'Not Set', 'Value Start Offset': 32, 'Value Size': 240, 'Object ID': {'ID': 'Logfile Information Table, dup.', 'Durable LSN Offset': 24, 'Buffer Offset': 200, 'Buffer Length': 0, 'Durable LSN': (0, 0), 'Page Reference': (4153, 0, 0, 0), 'Buffer Data': b''}}
{'Entry size': 272, 'Key Offset Start': 16, 'Key Size': 16, 'Flag': 'Not Set', 'Value Start Offset': 32, 'Value Size': 240, 'Object ID': {'ID': 'Logfile Information Table', 'Durable LSN Offset': 24, 'Buffer Offset': 200, 'Buffer Length': 0, 'Durable LSN': (0, 0), 'Page Reference': (4154, 0, 0, 0), 'Buffer Data': b''}}
[...snip...]
```
There is a flag that permits single entry output because there may occasionally be too many entries to view in the console.
```cmd
$> py main.py -f path/to/file.001 --node 33751040 --entry 1
```
```
{'Entry size': 272, 'Key Offset Start': 16, 'Key Size': 16, 'Flag': 'Not Set', 'Value Start Offset': 32, 'Value Size': 240, 'Object ID': {'ID': 'Logfile Information Table, dup.', 'Durable LSN Offset': 24, 'Buffer Offset': 200, 'Buffer Length': 0, 'Durable LSN': (0, 0), 'Page Reference': (4153, 0, 0, 0), 'Buffer Data': b''}}
```
### Note
The tables that populate the nodes have different structures so the output will be different for enery table, excluding the duplicates as they have the same structure as their parents.

# What's next?
- Adding support for the rest of the tables in the file system.
- Implementing ways to view the files/folders present in the forensic image. (Deleted or not)
- Adding the ability to recover deleted or non-deleted files/folders from the forensic image.
