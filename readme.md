# About the project
This idea started after I choose my university final year project and I learned that Microsoft has developed a new file system that removes some limitations that NTFS has and deals better with data corruption. After looking around to see if there are any tools or pieces of software 

The project is aiming to fit the needs of a day-to-day user and help out in data loss recovery, also I want to build a robust, powerful, and easy-to-use framework for forensic applications in which the logical/physical forensic image is formatted with ReFS.

# Current capabilities
- The ability to correctly parse and output information from the following:
    - Boot sector
    - Superblock
    - Checkpoint
    - Nodes

# Usage
For now, the tool will only be a command line/terminal utility but I haven't yet implemented the ability to pass flags to the script. With that said after cloning the repo please and acquiring your ReFS logical forensic image please modify line 9 in main.py with the path to your image.

# Giving credit where credit is due
This project wouldn't be possible or would be really hard to accomplish without the help of a paper written by Paul Prade, Tobias Groß, Andreas Dewald from Friedrich Alexander University
Erlangen-Nuremberg. Please feel free to go and read their amazing paper here -> https://doi.org/10.25593/issn.2191-5008/CS-2019-05