import logging
import os
import re
import binascii
import PyPDF2
import utils
import pdf_parsers
from extractors.extractor import Extractor
from PyPDF2.filters import *


class PdfExtractor(Extractor):
    def __init__(self, file_content, output):
        super().__init__(file_content, output)
        self.mapped_objects = dict()
        self.cmap_objects = dict()
        self.mapping_keys = dict()
        self.merged_cmap = dict()
        self.helper_pdf = 'helper.pdf'
        self.temp_pdf = 'temp.pdf'
        self.binary_to_replace = b'AABBAA'

    def extract_content(self):
        """
        Loop through pdf objects to find objects with interesting content
        :return:
        """
        pdf_objects = pdf_parsers.parse_to_objects(self.file_content)
        for obj_num in pdf_objects:
            obj = pdf_objects[obj_num]
            if (re.search(rb"/Subtype\s*/Image", obj)) and b"stream" in obj:
                self.extract_stream_image(obj, obj_num)
            elif b"/FlateDecode" in obj and b"stream" in obj:
                self.inspect_flate_object(obj, obj_num)

        if len(self.mapped_objects) > 0:
            for obj_num in self.mapped_objects:
                self.extract_text_mapped(obj_num)

    def extract_stream_image(self, pdf_object, obj_num):
        """
        extract image from pdf object
        :param pdf_object: the pdf object containing the image
        :param obj_num: the number of the object with image in it
        :return:
        """
        try:
            self.save_image_in_temp_pdf(pdf_object)
            self.extract_image(obj_num)
        except Exception as e:
            logging.error(f'{e} in obj number {obj_num}')

    def extract_image(self, obj_num):
        """
        extract the image
        :param obj_num: the number of the object
        """
        pdf = open('temp.pdf', 'rb')
        pdf_reader = PyPDF2.PdfReader(pdf)
        for page_num in range(0, len(pdf_reader.pages)):
            page_obj = pdf_reader.pages[page_num]
            try:
                xobject = page_obj['/Resources']['/XObject'].get_object()
            except:
                continue
            for obj in xobject:
                if xobject[obj]['/Subtype'] == '/Image':
                    mode = self.get_image_mode(xobject[obj]['/ColorSpace'])
                    image_stream = xobject[obj]
                    filter_array = image_stream.get("/Filter", ())
                    image_data = self.decode_image(image_stream._data, filter_array)
                    if '/DCTDecode' in filter_array:
                        utils.save_jpeg_image(image_data, mode, obj_num, self.output)
                    elif '/JPXDecode' in filter_array:
                        utils.save_jpeg2000_image(image_data, obj_num, self.output)
                    else:
                        utils.write_file(obj_num, image_data, self.output, "image")
        pdf.close()
        os.remove(self.temp_pdf)


    def save_image_in_temp_pdf(self, image_content):
        """
        saving the image in a temporary
        :param image_content: the image content
        """
        image_content = image_content[image_content.find(b'<<'):]
        pdf_helper = open(self.helper_pdf, 'rb')
        pdf_helper_content = pdf_helper.read()
        pdf_helper.close()
        temp_pdf_data = pdf_helper_content.replace(self.binary_to_replace, image_content)
        temp_pdf_file = open(self.temp_pdf, 'wb')
        temp_pdf_file.write(temp_pdf_data)
        temp_pdf_file.close()

    def decode_image(self, image_content, image_filter_array):
        """
        decoded the image by filter
        :param image_content: the byte array of the image
        :param image_filter_array: array of filters of the image
        :return: an image object
        """
        decoded_image = b""
        if '/FlateDecode' in image_filter_array:
            decoded_image = FlateDecode.decode(image_content)
        elif "/ASCIIHexDecode" in image_filter_array:
            decoded_image = ASCIIHexDecode.decode(image_content)
        elif "/LZWDecode" in image_filter_array:
            decoded_image = LZWDecode.decode(image_content)
        elif "/ASCII85Decode" in image_filter_array:
            decoded_image = ASCII85Decode.decode(image_content)
        return decoded_image if decoded_image != b'' else image_content

    def get_image_mode(self, color_space):
        """
        return the image mode
        :param color_space: the color space of the image
        :return: the mode of the image
        """
        mode = ""
        if color_space == '/DeviceRGB':
            mode = "RGB"
        elif color_space == '/DeviceCMYK':
            mode = "CMYK"
        elif color_space == '/DeviceGray':
            mode = "L"
        elif color_space == "/Indexed" or color_space == "/ICCBased":
            mode = "P"
        return mode

    def inspect_flate_object(self, pdf_object, obj_num):
        """
        inspect flate object to find text or cmaps
        :param pdf_object: the pdf object containing the deflated content
        :param obj_num: the number of the object to be inspected
        :return:
        """
        text_content = pdf_object.split(b"stream")[1][:-3].strip()
        text_content = utils.flate_decode(text_content, obj_num)
        if obj_num == 2:
            pass
        if text_content is not None:
            if b"BT" in text_content and b"ET" in text_content:
                if b"(" in text_content:
                    self.extract_text_unmapped(obj_num, text_content)
                elif b"<" in text_content:
                    self.mapped_objects[obj_num] = text_content
            elif b"beginbfchar" in text_content:
                self.cmap_objects[obj_num] = pdf_parsers.parse_cmap(text_content, self.merged_cmap)

    def extract_text_unmapped(self, obj_num, text_content):
        """
        extract all text in text object that doesn't use cmaps
        :param obj_num: the number of the object with the text that wasn't mapped
        :param text_content: the deflated content of the text object
        :return:
        """
        extracted_text = b""
        s = text_content[text_content.find(b"BT"): text_content.rfind(b"ET")]
        to_extract = False
        for i in range(len(s)):
            if s[i] == ord(b"(") and s[i - 1] != ord(b"\\"):
                to_extract = True
            elif s[i] == ord(b")") and s[i - 1] != ord(b"\\"):
                to_extract = False
            elif to_extract:
                extracted_text += s[i].to_bytes(1, 'big')

        if len(extracted_text.strip()) > 0:
            utils.write_file(obj_num, extracted_text, self.output, "text")

    def extract_text_mapped(self, obj_num):
        """
        extract all text in text object that uses cmaps
        :param obj_num: the number of the object with the mapped text
        :return:
        """
        mapped_content = pdf_parsers.parse_mapped_content(self.mapped_objects[obj_num])
        should_try_hex = True
        for key_value in self.merged_cmap:
            try:
                extracted_text = self.get_extracted_text(mapped_content, key_value, obj_num)
                if len(extracted_text) > 0:
                    utils.write_file(obj_num, extracted_text, self.output, "text", cmap_len=key_value)
                    should_try_hex = False
            except Exception as e:
                logging.error(f'error: {e}, object number:{obj_num}, key length:{key_value}')
        if should_try_hex:
            # try hex mapping
            try:
                hex_mapped_content = binascii.unhexlify(mapped_content).replace(b"\x00", b"")
                utils.write_file(obj_num, hex_mapped_content, self.output, "text", cmap_len="hex")
            except Exception as e:
                logging.error(f'error while trying to do hex mapping: {e}, object number:{obj_num}')

    def get_extracted_text(self, mapped_content, key_len, obj_num):
        """
        extract the text.
        :param mapped_content: the mapped content
        :param key_len: the length of the key
        :param obj_num: the number of the object
        :return: the text of the object
        """
        unmapped_content = b""
        mapped_array = self.get_mapped_keys(mapped_content, key_len, obj_num)
        for key_value in mapped_array:
            if key_value in self.merged_cmap[key_len]:
                unmapped_content += self.merged_cmap[key_len][key_value]
            else:
                logging.debug(f"Could not find key:{key_value} in cmaps with the length of {key_len}")
        extracted_text = binascii.unhexlify(unmapped_content)
        decoded_extracted_text = extracted_text.decode('utf-16-be')
        return decoded_extracted_text.encode('utf-8')

    def get_mapped_keys(self, mapped_content, key_len, obj_num):
        """
        break mapped data into chucks of size key length so the mapped data can be unmapped
        save the breakdown into mapping keys to avoid having to repeat the same breakdown over and over
        :param mapped_content: the mapped content to break into chunks
        :param key_len: the len of the cmap keys
        :param obj_num: the number of the object (unique)
        :return: the mapped data broken down into chunks of size cmap key length
        """
        if obj_num not in self.mapping_keys:
            self.mapping_keys[obj_num] = [mapped_content[i: i + key_len] for i in
                                          range(0, len(mapped_content), key_len)]
        return self.mapping_keys[obj_num]
