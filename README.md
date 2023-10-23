# White Phoenix
![White-Phoenix-logo](https://github.com/2niknatan/White-Phoenix/assets/109152039/2f34f624-1c53-4c2c-9716-3543f29dfa65)

This tool recovers content from files encrypted by Ransomware using “intermittent encryption”

For more details please visit our blog post:
https://www.cyberark.com/resources/threat-research-blog/white-phoenix-beating-intermittent-encryption


# Example:



https://github.com/2niknatan/White-Phoenix/assets/109152039/3fe5ddd3-7f6c-4763-88a7-ae96bc637bfd



Tested on:
    BlackCat/ALPHV Ransomware, Play Ransomware, Qilin/Agenda Ransomware, BianLian Ransomware, DarkBit

Usage:
    python3 White-Phoenix.py [-h] [-f/--file FILE] [-s/--separated-files] [-dl/--disable-log] [-d/--dir] [-v/--virtual-machine] -o/--output FOLDER 

    -f/--file : path to the encrypted file
    -o/--output : path to folder to save the content extracted from the file
    -s/--separated-files : extract the content to separated files
    -dl/--disale-log : disable the log
    -d/--dir : start scanning from a specific path
    -v/--virtual machine: Extract files from encrypted virtual machines
    

Currently supported filetypes include:
    'pdf', 
    'docx', 'docm', 'dotx', 'dotm', 'odt',
    'xlsx', 'xlsm', 'xltx', 'xltm', 'xlsb', 'xlam', 'ods'
    'pptx', 'pptm', 'ptox', 'potm', 'ppsx', 'ppsm', 'odp'
    'zip'


### Output files

**PDF:**
By default, the output is saved to docx file to allow for editing.<br>
However, sometimes images are not able to load in the docx, so there is an option the save the files separately.<br>
Each object is saved as a seperate file with the object number used as the file name.<br>
Text objects that use cmap have multiple files created for every possible mapping found in the file as well as a possible hex mapping.<br>
Cmap text objects have an aditional part of the name to indicate which mapping was used.<br>
Please note this means that many cmap files will either have meaningless content or possibly duplicates content.<br>
Not all image filters are supported however all the image objects are extracted, this means that not all the images are usable.



**Office**

- **Word**

    - [output folder]/word/document.xml - Text content
    - [output folder]/word/media - Images

- **Excel**

    - [output folder]/xl/worksheets/ - Sheets content
    - [output folder]/xl/sharedStrings.xml - Sheets strings
    - [output folder]/xl/media - Images

- **PowerPoint**

    - [output folder]/ppt/slides/ - Slides content
    - [output folder]/ppt/media - Images

- **Open Office (odt, ods, odp)**
    - [output folder]/content.xml - content of various types
    - [output folder]/media - Images


### Virtual Machines Support
Many ransomware groups maintain a variant of their ransomware specifically meant to target VMs on ESXi servers. White Phoenix has a
feature to recover data from encrypted vm files. To use the vm feature simply run white phoenix with the flag -v or 
--virtual-machine on files that represent either memory or storage of the virtual machines such as files with the extension vmem or vmdk.
White Phoenix uses file carving to identify unencrypted files and extract them to disk. The vm support works with both the -f and -d flags
to either run on a single file or and entire folder respectively.
Please keep in mind that in this method White Phoenix has no way of knowing the names of the files it recovering. Additionally, many files
are stored on disks and in memory in a somewhat corrupt manner so not everything will be readable once extracted. In some cases files that
were extrated but aren't readable still contain data that can be recovered by white phoenix. So a file is extracted but not readable it
might be worth trying to run white phoenix a second time on the newly extracted file.

Supported types for vms:<br>
- pdf
- zip
- ooxml
    - docx
    - xlsx
    - pptx
- jpg
- gif

**Other File Types**

Adding more file types for VMs is relatively simple. What you'll need is the file extension, file magic/header/signature aka the first few 
bytes for that file type, and file ending/footer. A lot of file magics can be found in https://en.wikipedia.org/wiki/List_of_file_signatures. 
Alternatively, you can create a file of the type you're interested in and open it with a hex editor to see the first few bytes. 
The ending can be trickier to find. Some googling might help or you can try the hex editor again and of course there's chatGPT. 
If you can't find a footer you can use a large collection of null bytes.<br>
Once you find all the values, open the vm_files.config found in the extractors folder and update it. The file is a simple json format.
Keep in mind that the header and footer values are treated as regex values in the code so if you find more than 1 possible value you can use a single entry in the json.


### License and Copyright


Please note: This tool is provided as is, and subject to the Apache License Version 2.0. It is not 100% effective and has a greater chance of success when running on larger files.

Copyright (c) 2023 CyberArk Software Ltd. All rights reserved.
