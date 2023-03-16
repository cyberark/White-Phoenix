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

Please note: This tool is provided as is, and subject to the Apache License Version 2.0. It is not 100% effective and has a greater chance of success when running on larger files.

Copyright (c) 2023 CyberArk Software Ltd. All rights reserved.
