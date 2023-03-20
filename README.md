This tool recovers content from files encrypted by Ransomware using “intermittent encryption”

Tested on:
    BlackCat/ALPHV Ransomware, Play Ransomware, Qilin/Agenda Ransomware, BianLian Ransomware, DarkBit

Usage:
    python3 White-Phoenix.py [-h] -f/--file FILE -o/--output FOLDER 

    -f/--file : path to the encrypted file
    -o/--output : path to folder to save the content extracted from the file

Currently supported filetypes include:
    'pdf', 
    'docx', 'docm', 'dotx', 'dotm', 'odt',
    'xlsx', 'xlsm', 'xltx', 'xltm', 'xlsb', 'xlam', 'ods'
    'pptx', 'pptm', 'ptox', 'potm', 'ppsx', 'ppsm', 'odp'
    'zip'


For PDF documents:

    Each object is saved as a seperate file with the object number used as the file name.
    Text objects that use cmap have multiple files created for every possible mapping found in the file as well as a possible hex mapping.
    Cmap text objects have an aditional part of the name to indicate which mapping was used.
    Please note this means that many cmap files will either have meaningless content or possibly duplicates content.
    Not all image filters are supported however all the image objects are extracted, this means that not all the images are usable.



For Office documents:

    Images will appear in a folder named media. Depending on the format the folder will either be a subfolder of the folder word or xl or ppt.
    
    For Word Documents, we can find the text in the following xml file:
    
        [output folder]/word/document.xml
    
    Excel Documents store their sheets in the folder:
    
        [output folder]/xl/worksheets/
        
        However, text used in the sheets is often stored in a separate file:
        
        [output folder]/xl/sharedStrings.xml
    
    For PowerPoint Documents, the slides are stored in the folder:
        
        [output folder]/ppt/slides/      
        
    For Open Office files (odt, ods, odp) the text will appear in a file called content.xml directly in the output folder.
    Images also appear in a folder called media but for these formats it will be directly in the output folder.



Please note: This tool is provided as is, and subject to the Apache License Version 2.0. It is not 100% effective and has a greater chance of success when running on larger files.

Copyright (c) 2023 CyberArk Software Ltd. All rights reserved.
