This tool is meant to be a decryptor for files encrypted by BlackCat Ransomware

Usage:
    python3 main.py [-h] -f/--file FILE -o/--output FOLDER -t/--type FILETYPE

    -f/--file : path to the encrypted file
    -o/--output : path to folder to save the content extracted from the file
    -t/--type : type of encrypted file

Currently supported filetypes include:
    'pdf', 
    'docx', 'docm', 'dotx', 'dotm', 'odt',
    'xlsx', 'xlsm', 'xltx', 'xltm', 'xlsb', 'xlam', 'ods'
    'pptx', 'pptm', 'ptox', 'potm', 'ppsx', 'ppsm', 'odp'
    'zip'
