import zlib
import logging
import os
from argparse import ArgumentParser
import winreg
import tkinter as tk


def create_eula():
    """
    Create a EULA window and updage a registry key when accepted
    """
    EULA_ACCEPTED_REG_KEY = r"SOFTWARE\White Phoenix"
    EULA_ACCEPTED_REG_VALUE = "EULAAccepted"
    EULA_Title = "End User License Agreement (EULA)"
    EULA_TEXT = """\


This is the End User License Agreement (EULA) for the software product developed by XYZ Corp. Please read this agreement carefully before using the software. 

By using the software, you agree to be bound by the terms of this EULA. If you do not agree to the terms of this EULA, do not use the software.

1. License
XYZ Corp. grants you a limited, non-exclusive license to use the software for personal or commercial purposes.

2. Ownership
The software and all intellectual property rights, including but not limited to copyrights and trademarks, are owned by XYZ Corp.

3. Restrictions
You may not copy, modify, distribute, sell, or transfer the software or any portion thereof without the prior written consent of XYZ Corp.

4. Disclaimer of Warranties
The software is provided "as is" without warranty of any kind, either express or implied, including, but not limited to, the implied warranties of merchantability and fitness for a particular purpose.

5. Limitation of Liability
In no event shall XYZ Corp. be liable for any direct, indirect, incidental, special, or consequential damages arising out of or in connection with the use or inability to use the software.

6. Termination
This EULA is effective until terminated. You may terminate this EULA at any time by uninstalling the software.

7. Governing Law
This EULA shall be governed by and construed in accordance with the laws of the state of California.

    """
    
    
    # Create the main window
    eula_window = tk.Tk()
    eula_window.title("End User License Agreement")
    eula_window.geometry("600x600")

    # Create a text widget to display the EULA text
    eula_text = tk.Text(eula_window, wrap="word")
    eula_text.insert(tk.END, EULA_Title, "bold")
    eula_text.insert(tk.END, EULA_TEXT)
    eula_text.tag_configure("bold", font=("bold", 14))
    eula_text.pack(fill="both", padx=10, pady= 10, expand=True)

    # Create a button to accept the EULA and close the popup window
    def accept_eula():
        key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, EULA_ACCEPTED_REG_KEY)
        winreg.SetValueEx(key, EULA_ACCEPTED_REG_VALUE, 0, winreg.REG_DWORD, 1)
        winreg.CloseKey(key)
        eula_window.destroy()
    
    #Create Decline Button
    accept_button = tk.Button(eula_window, text="Decline", command=exit)
    accept_button.pack(side=tk.RIGHT, padx=5, pady= 5)
    #Create Accept Button
    accept_button = tk.Button(eula_window, text="Accept", command=accept_eula)
    accept_button.pack(side=tk.RIGHT, pady= 5)

    
    eula_window.mainloop()

def EULA():
    """
    Check if EULA was agreed upon
    If not call creat_eula
    """
    EULA_ACCEPTED_REG_KEY = r"SOFTWARE\White Phoenix"
    key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, EULA_ACCEPTED_REG_KEY)
    value = winreg.QueryInfoKey(key)
    if value[1] != 1:
        create_eula()


def argparse():
    """
    parse the argument to find path of file to extract info from
    :return: arguments
    """
    parser = ArgumentParser(description="Recover text and images from partially encrypted files")
    parser.add_argument("-f", "--file", required=True, dest="filename", metavar="FILE",
                        help="Path to encrypted file")
    parser.add_argument("-o", "--output", required=True, dest="output", metavar="FOLDER",
                        help="Path to folder to save extracted content")
    return parser.parse_args()


def verify_output(output_path):
    """
    verify the output folder exists, if not try to create the path
    :param output_path: the output path given as a parameter
    :return:
    """
    if not os.path.exists(output_path):
        try:
            os.mkdir(output_path)
        except OSError as e:
            logging.error(f"Error creating output folder:{e}")
            exit(-1)


def init_logger():
    """
    creates a logger
    :return:
    """
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')


def find_object_number(obj_start, content):
    """
    find the number of the object found
    :param obj_start: address of the obj at the start of the object
    :param content: the content of the whole pdf file
    :return: the number of the object found
    """
    object_declaration_row_addr = max(content[: obj_start].rfind(b"\n"), content[: obj_start].rfind(b"\r"))
    object_declaration_row = content[object_declaration_row_addr + 1: obj_start]
    obj_num = int(object_declaration_row.split(b" ")[0])
    logging.info(f"Found object number {obj_num:5} at offset: {hex(object_declaration_row_addr)}")
    return obj_num


def flate_decode(compressed_stream, obj_num):
    """
    decompress extracted stream
    :param compressed_stream: compressed stream, should only contain the actual stream and not the full object
    :param obj_num: the object number of the compressed object
    :return: the decompressed stream or None if fail
    """
    try:
        logging.info(f"Found DEFLATE at object {obj_num}")
        content = zlib.decompress(compressed_stream)
        return content
    except Exception as e:
        logging.error(f"Error decompressing:{e}")
        return None


def read_file(filename):
    """
    read encrypted pdf file
    :param filename: path to encrypted pdf file
    :return: file content
    """
    try:
        with open(filename, "rb") as f:
            content = f.read()
    except FileNotFoundError as e:
        logging.error(f"Error opening file: {e}")
        exit(-1)
    return content


def write_file(obj_num, file_content, output_path, file_type, cmap=None):
    """
    write extracted content to file
    :param obj_num: the object from which the content was extracted
    :param file_content: the content of the file to write
    :param output_path: the path to the output folder where the extracted content is to be written
    :param file_type: the type of file image or text
    :param cmap: if text was decoded with cmap, this is the object number of the cmap
    :return:
    """
    file_name = get_file_name(obj_num, file_type, cmap)
    with open(f"{output_path}/{file_name}", "wb") as f:
        f.write(file_content)
    log = f"Extracted {file_type} content from object {obj_num}" if (cmap is None) else \
        f"Extracted {file_type} content from object {obj_num} with cmap from {cmap}"
    logging.info(log)


def get_file_name(obj_num, file_type, cmap):
    """
    build a file name for a file to be written
    :param obj_num: the object from which the content was extracted
    :param file_type: the type of file image or text
    :param cmap: if text was decoded with cmap, this is the object number of the cmap
    :return: file name
    """
    file_types = {
        "image": ".jpg",
        "text": ".txt"
    }
    file_name = str(obj_num)
    if cmap is not None:
        file_name += '_cmap_' + str(cmap)
    file_name += file_types[file_type]
    return file_name
