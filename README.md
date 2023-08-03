# White Phoenix

This tool recovers content from files encrypted by Ransomware using “intermittent encryption” based on the [White Phoenix: Beating Intermittent Encryption](https://www.cyberark.com/resources/threat-research-blog/white-phoenix-beating-intermittent-encryption) research.

Tested on:<br>
BlackCat/ALPHV Ransomware, Play Ransomware, Qilin/Agenda Ransomware, BianLian Ransomware, DarkBit

Usage:
```
usage: White-Phoenix.py [-h] [-f FILE] -o FOLDER [-s] [-dl] [-d OLDER]

Recover text and images from partially encrypted files

options:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  Path to encrypted file
  -o FOLDER, --output FOLDER
                        Path to folder to save extracted content
  -s, --separated-files
                        Extract to separate files
  -dl, --disable-log    Disable the log
  -d FOLDER, --dir FOLDER
                        Check for files recursively from a specific folder
```
    

Currently supported filetypes include:
* pdf
* docx, docm, dotx, dotm, odt
* xlsx, xlsm, xltx, xltm, xlsb, xlam, ods
* pptx, pptm, ptox, potm, ppsx, ppsm, odp
* zip


### Output files

**PDF:**<br>
By default, the output is saved to docx file to allow for editing.<br>
However, sometimes images are not able to load in the docx, so there is an option the save the files separately.<br>
Each object is saved as a seperate file with the object number used as the file name.<br>
Text objects that use cmap have multiple files created for every possible mapping found in the file as well as a possible hex mapping.<br>
Cmap text objects have an aditional part of the name to indicate which mapping was used.<br>
Please note this means that many cmap files will either have meaningless content or possibly duplicates content.<br>
Not all image filters are supported however all the image objects are extracted, this means that not all the images are usable.

<br>

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


### License and Copyright


Please note: This tool is provided as is, and subject to the Apache License Version 2.0. It is not 100% effective and has a greater chance of success when running on larger files.

Copyright (c) 2023 CyberArk Software Ltd. All rights reserved.
