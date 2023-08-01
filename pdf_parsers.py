import logging
import utils
import re


def parse_to_objects(content):
    """
    Find all pdf objects that weren't encrypted
    :param content: the content of the encrypted pdf file
    :return: pdfs_object dictionary containing all the objects successfully extracted from the pdf
    """

    pdf_objects = dict()

    # regex to find start of pdf object "\d+ 0 obj" followed by content of object followed by end of object "endobj"
    objects_regex = re.compile(b"\D(\d+ 0 obj.*?endobj)", re.S)
    pdf_object = re.search(objects_regex, content)
    start_addr = 0
    while pdf_object:
        obj_num = int(pdf_object.group(1).split(b" ")[0])
        start_addr += pdf_object.start() + 1
        logging.info(f"Found object {obj_num} at offset {hex(start_addr)}")
        pdf_objects[obj_num] = pdf_object.group(1)
        pdf_object = re.search(objects_regex, content[start_addr:])

    logging.info(f"Found a total of {len(pdf_objects)} objects")

    return pdf_objects


def parse_cmap(text_content, merged_cmap):
    """
    parses cmap object to create a character mapping for text objects that rely on cmaps
    :param text_content: the content of the cmap object
    :return:

    the main part of character mapping appears as follows:
    beginbfchar
    <key1><value1>
    <key2><value2>
    ...
    endbfchar

    with the characters in the keys and values represented as hex values
    the loop extracts all the keys and matching values and saves them in the cmap_objects dictionary
    """
    key = None
    cmap_content = text_content[text_content.find(b"beginbfchar") + len(b"beginbfchar"):
                                text_content.find(b"endbfchar")].strip(b"\n")
    cmap_list = cmap_content.split(b"\n")  # each entry contains a cmap key value pair
    cmap_dict = dict()

    for cmap_entry in cmap_list:
        key = cmap_entry[1: cmap_entry.find(b">")].upper()
        value = cmap_entry[cmap_entry.rfind(b"<") + 1: -1].upper()
        cmap_dict[key] = value

    if key is not None:
        if len(key) in merged_cmap:
            merged_cmap[len(key)].update(cmap_dict)
        else:
            merged_cmap[len(key)] = cmap_dict
        return cmap_dict


def parse_mapped_content(mapped_object):
    """
    find all mapped content in mapped objects and concatenate them together
    :param mapped_object: the data from the mapped object
    :return: the mapped content extracted from the mapped object
    """
    mapped_content = b""
    mapped_content_reqex = re.compile(b".*?<(.*?)>.*?", re.S)
    for mapped_content_part in mapped_content_reqex.findall(mapped_object):
        mapped_content += mapped_content_part
    return mapped_content
