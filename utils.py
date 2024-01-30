import zlib
import logging
import os
from argparse import ArgumentParser
from io import BytesIO
from PIL import Image
import numpy as np

logo = """
⠀⠠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⠀⠀⠀⠀⠀
⠀⢸⢠⠀⣄⢣⡀⠀⢦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠨⡀⠀⠠⡑⡀⢀⠀⠀⠀
⠀⢸⠜⣦⣻⢮⢧⢀⢸⢪⡂⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢐⢐⠀⢕⠐⠠⡢⠀⠀⠀
⠀⢘⢏⡺⣪⢫⣟⢐⢸⢕⡇⡇⡀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡂⡂⡊⡂⡌⡪⠂⡀⠀⠀
⠀⠈⠳⣺⢝⣗⣗⡇⡮⡳⣝⡅⡧⡣⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡐⡐⡐⡜⡌⡎⢎⠔⣠⠀⠀
⠀⠀⠀⠈⠓⢗⢵⢝⢜⢽⢸⡪⣺⠸⡡⣀⠀⠀⠀⠀⠀⠀⠅⡐⡐⡐⢌⠎⡊⡌⣆⢏⠊⠀⠀
⠀⠀⠀⠀⠀⠀⠙⢜⢜⢜⢔⢕⢕⢜⠜⡢⡂⠂⠀⡀⠠⠨⡐⡐⡐⡌⡆⣇⠧⣓⠡⠅⠆⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠈⢪⢪⢪⠪⡪⡢⡱⡨⡊⡢⢐⠠⢑⠕⢔⣊⢆⢦⣪⢎⣞⣜⢭⠤⠄⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢣⠣⡣⡑⢌⠢⡊⡢⠨⡔⡕⡕⣍⠲⢴⢕⣝⢯⢟⠷⠫⠗⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⡐⡀⠄⡑⡐⡈⡂⡑⣐⣠⢳⡳⣵⢕⡶⣟⢗⢿⣚⡹⠵⣟⠦⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢀⢂⢢⢑⠰⢐⢐⡐⢄⢓⡕⣟⢮⢯⢻⡟⡎⢯⢯⢯⡻⠶⡄⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢢⠃⠉⢮⡢⡑⡊⠢⠨⡚⡸⡘⢎⢲⠙⡽⡸⢌⢷⡙⠆⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢮⣮⢊⢂⢆⢂⠻⢔⠐⢧⠘⠍⠈⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⡆⢆⣆⡂⠅⠢⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⢔⠒⡚⠢⠩⡢⠡⢑⢢⠨⢐⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠀⠀⠈⠪⡿⡐⠄⡑⡐⡐⡈⡐⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠻⢘⠐⡐⠄⢂⠢⡐⢐⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠂⠑⠀⠀⠁⠈⠂⠈⠀⠀⠀⠀⠀⠀⠀
"""


def argparse():
    """
    parse the argument to find path of file to extract info from
    :return: arguments
    """
    parser = ArgumentParser(description="Recover text and images from partially encrypted files")
    parser.add_argument("-f", "--file", required=False, dest="filename", metavar="FILE",
                        help="Path to encrypted file")
    parser.add_argument("-o", "--output", required=True, dest="output", metavar="FOLDER",
                        help="Path to folder to save extracted content")
    parser.add_argument("-s", "--separated-files", required=False, dest="separated_files", action='store_true',
                        help="Extract to separate files")
    parser.add_argument("-v", "--virtual-machine", required=False, dest="vm", action='store_true',
                        help="Extract files from encrypted virtual machines")
    parser.add_argument("-dl", "--disable-log", required=False, dest="disable_log", action='store_true',
                        help="Disable the log")
    parser.add_argument("-d", "--dir", required=False, dest="dir", metavar="FOLDER",
                        help="Check for files recursively from a specific folder")
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


def init_logger(disable_logger):
    """
    creates a logger
    :return:
    """
    if disable_logger is True:
        logging.disable()
    else:
        logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(threadName)s: %(message)s')
        logging.info(logo)
        logging.info("Copyright © 2023 CyberArk Software Ltd. All rights reserved.\n\n")


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


def write_raw_file(image_data, obj_num, output, file_name, extension=None):
    """
    save binary as is in file
    :param image_data: the binary of the image
    :param obj_num: the number of the object
    :param output: the output path of the file
    :param extension: the extension of the file
    """
    if extension is None:
        extension = '.jpg'
    save_path = os.path.join(output, file_name, str(obj_num) + extension)
    image = open(save_path, "wb")
    image.write(image_data)
    image.close()
    return save_path


def decode_content(file_content):
    """
    decode text content
    :param file_content: the text content of the file
    :return: return decoded content of the text if succeeded empty if not
    """
    content = ""
    encodings_to_try = [
        'utf-8', 'latin-1', 'utf-16', 'ascii', 'utf-32', 'cp1252', 'iso-8859-1', 'mac_roman',
        'utf-16-le', 'utf-16-be', 'utf-7', 'utf-9', 'utf-1', 'utf-32-le', 'utf-32-be',
        'big5', 'big5hkscs', 'cp037', 'cp273', 'cp424', 'cp437', 'cp500', 'cp775', 'cp850', 'cp852',
        'cp855', 'cp857', 'cp858', 'cp860', 'cp861', 'cp862', 'cp863', 'cp864', 'cp865', 'cp866',
        'cp869', 'cp874', 'cp875', 'cp932', 'cp949', 'cp950', 'euc_jp', 'euc_jis_2004', 'euc_jisx0213',
        'euc_kr', 'gb2312', 'gbk', 'hz', 'iso2022_jp', 'iso2022_jp_1', 'iso2022_jp_2', 'iso2022_jp_2004',
        'iso2022_jp_3', 'iso2022_jp_ext', 'iso2022_kr', 'iso8859_2', 'iso8859_3', 'iso8859_4', 'iso8859_5',
        'iso8859_6', 'iso8859_7', 'iso8859_8', 'iso8859_9', 'iso8859_10', 'iso8859_11', 'iso8859_13',
        'iso8859_14', 'iso8859_15', 'iso8859_16', 'koi8_r', 'koi8_u', 'mbcs', 'ptcp154', 'shift_jis',
        'shift_jis_2004', 'shift_jisx0213', 'tactis', 'tis-620', 'utf_7', 'utf_8_sig'
    ]
    for encoding in encodings_to_try:
        try:
            content = file_content.decode(encoding)
            break
        except Exception as e:
            logging.info(f"Failed to decode using {e}")
            content = ""
    return content


def write_to_file(obj_num, file_content, output_path, file_type, separated_files, document, filter_array=None,
                  mode=None, cmap_len=None, file_name=None):
    """
    write extracted content to file
    :param obj_num: the object from which the content was extracted
    :param file_content: the content of the file to write
    :param output_path: the path to the output folder where the extracted content is to be written
    :param file_type: the type of file image or text
    :param separated_files: boolean for saving in separated files or in docx file
    :param document: a document object
    :param filter_array: the filters of an image
    :param mode: the mode of the image
    :param cmap_len: if text was decoded with cmap, this is the length of the bytes in the cmaps
    :param file_name: the name of the file
    :return:
    """
    if file_type == "text":
        content = decode_content(file_content)
        if separated_files:
            dir_path = os.path.join(output_path, os.path.split(file_name)[-1].replace('.', '_'))
            if not os.path.exists(dir_path):
                os.mkdir(os.path.join(dir_path))
            try:
                with open(os.path.join(dir_path, str(obj_num) + '.txt'), 'w+') as txt_file:
                    txt_file.write(content)
            except:
                pass
        else:
            try:
                document.add_paragraph(content)
            except:
                logging.error(f"Couldn't insert object number {obj_num} to docx file")
    else:
        if '/DCTDecode' in filter_array:
            file_path = save_jpeg_image(file_content, mode, obj_num, output_path,
                                                   os.path.split(file_name)[-1].replace('.', '_'))
        elif '/JPXDecode' in filter_array:
            file_path = write_raw_file(file_content, obj_num, output_path,
                                                  os.path.split(file_name)[-1].replace('.', '_'), '.jp2')
        else:
            file_path = write_raw_file(file_content, obj_num, output_path,
                                                  os.path.split(file_name)[-1].replace('.', '_'))
        if separated_files is not True:
            try:
                document.add_paragraph()
                document.add_picture(file_path)
            except Exception as e:
                logging.error(f"{e}: Couldn't add object number {str(obj_num)} to docx")
            os.remove(file_path)

    log = f"Extracted {file_type} content from object {obj_num}" if (cmap_len is None) else \
        f"Extracted {file_type} content from object {obj_num} with cmap from {cmap_len}"
    logging.info(log)


def save_jpeg_image(image_content, mode, obj_num, output, file_name):
    """
    get jpeg image object
    :param image_content: the byte array of the image
    :param mode: mode of the image
    :param obj_num: the number of the object
    :param output: the output path of the file
    :param file_name: the name of the file
    """
    jpg_data = BytesIO(image_content)
    try:
        image = Image.open(jpg_data)
    except:
        return
    if mode == "CMYK":
        im_data = np.frombuffer(image.tobytes(), dtype='B')
        inv_data = np.full(im_data.shape, 255, dtype='B')
        inv_data -= im_data
        image = Image.frombytes(image.mode, image.size, inv_data.tobytes())
    save_path = os.path.join(output, file_name)
    os.makedirs(save_path, exist_ok=True)
    save_path = os.path.join(save_path, str(obj_num) + ".jpg")
    image.save(save_path)
    image.close()
    return save_path


def save_doc_file(output, filename, document):
    """
    save to docx file
    :param output: the output path of the file
    :param filename: the name of the file
    :param document: type var of docx
    """
    dir_path = os.path.join(output, os.path.split(filename)[-1].replace('.', '_'))
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    document.save(os.path.join(dir_path, os.path.split(filename)[-1].replace('.', '_') + '.docx'))
