# White Phoenix

This tool recovers content from files encrypted by Ransomware using “intermittent encryption”

Tested on:
    BlackCat/ALPHV Ransomware, Play Ransomware, Qilin/Agenda Ransomware, BianLian Ransomware, DarkBit

Usage:
    python3 White-Phoenix.py [-h] -f/--file FILE -o/--output FOLDER 

    -f/--file : path to the encrypted file
    -o/--output : path to folder to save the content extracted from the file
    -s/--separated-files : extract the content to separated files
    -dl/--disale-log : disable the log
    -d/--dir : start scanning from a specific path
    

Currently supported filetypes include:
    'pdf', 
    'docx', 'docm', 'dotx', 'dotm', 'odt',
    'xlsx', 'xlsm', 'xltx', 'xltm', 'xlsb', 'xlam', 'ods'
    'pptx', 'pptm', 'ptox', 'potm', 'ppsx', 'ppsm', 'odp'
    'zip'


### Output files

**PDF:**
By default, the output is saved to docx file to allow for editing.
However, sometimes images are not able to load in the docx, so there is an option the save the files separately.
Each object is saved as a seperate file with the object number used as the file name.
Text objects that use cmap have multiple files created for every possible mapping found in the file as well as a possible hex mapping.
Cmap text objects have an aditional part of the name to indicate which mapping was used.
Please note this means that many cmap files will either have meaningless content or possibly duplicates content.
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


### License and Copyright


Please note: This tool is provided as is, and subject to the Apache License Version 2.0. It is not 100% effective and has a greater chance of success when running on larger files.

Copyright (c) 2023 CyberArk Software Ltd. All rights reserved.
