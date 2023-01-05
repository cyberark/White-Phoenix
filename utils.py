import zlib
import logging
import os
from argparse import ArgumentParser

def argparse():
    """
    parse the argument to find path of file to extract info from
    :return: arguments
    """
    parser = ArgumentParser(description="Recover text and images from partially encrypted PDF files")
    parser.add_argument("-f", "--file", required=True, dest="filename", metavar="FILE",
                        help="Path to encrypted PDF file")
    parser.add_argument("-o", "--output", required=True, dest="output", metavar="FOLDER",
                        help="Path to folder to save extracted content")
    parser.add_argument("-t", "--type", required=True, dest="type", help="Type of encrypted file")
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
