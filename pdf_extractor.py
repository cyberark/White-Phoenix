import re
import binascii
import utils
import pdf_parsers
from extractor import Extractor


class PdfExtractor(Extractor):
    def __init__(self, filename, output):
        super().__init__(filename, output)
        self.mapped_objects = dict()
        self.cmap_objects = dict()
        self.mapping_keys = dict()

    def extract_content(self):
        """
        Loop through pdf objects to find objects with interesting content
        :return:
        """
        pdf_objects = pdf_parsers.parse_to_objects(self.filename)
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
        image_content = pdf_object.split(b"stream")[1][:-3].strip()
        if b"FlateDecode" in pdf_object:
            image_content = utils.flate_decode(image_content, obj_num)
        # check content exists and isn't "junk" starting with null bytes
        if image_content is not None and image_content[:4] != b"\x00" * 4:
            utils.write_file(obj_num, image_content, self.output, "image")

    def inspect_flate_object(self, pdf_object, obj_num):
        """
        inspect flate object to find text or cmaps
        :param pdf_object: the pdf object containing the deflated content
        :param obj_num: the number of the object to be inspected
        :return:
        """

        text_content = pdf_object.split(b"stream")[1][:-3].strip()
        text_content = utils.flate_decode(text_content, obj_num)
        if text_content is not None:
            if b"BT" in text_content and b"ET" in text_content:
                if b"(" in text_content:
                    self.extract_text_unmapped(obj_num, text_content)
                elif b"<" in text_content:
                    self.mapped_objects[obj_num] = text_content
            elif b"beginbfchar" in text_content:
                self.cmap_objects[obj_num] = pdf_parsers.parse_cmap(text_content)

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
            if s[i] == ord(b"(") and s[i-1] != ord(b"\\"):
                to_extract = True
            elif s[i] == ord(b")") and s[i-1] != ord(b"\\"):
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

        # try hex mapping
        hex_mapped_content = binascii.unhexlify(mapped_content).replace(b"\x00", b"")
        utils.write_file(obj_num, hex_mapped_content, self.output, "text", cmap="hex")

        # try mappings from cmap objects
        for cmap in self.cmap_objects:
            unmapped_content = b""
            mapped_array = self.get_mapped_keys(mapped_content, self.cmap_objects[cmap])

            for key_value in mapped_array:
                if key_value in self.cmap_objects[cmap]:
                    unmapped_content += self.cmap_objects[cmap][key_value]
            extracted_text = binascii.unhexlify(unmapped_content).replace(b"\x00", b"")
            if len(extracted_text) > 0:
                utils.write_file(obj_num, extracted_text, self.output, "text", cmap=cmap)

    def get_mapped_keys(self, mapped_content, cmap):
        """
        break mapped data into chucks of size key length so the mapped data can be unmapped
        save the breakdown into mapping keys to avoid having to repeat the same breakdown over and over
        :param mapped_content: the mapped content to break into chunks
        :param cmap: the cmap dict containing the key length
        :return: the mapped data broken down into chunks of size cmap key length
        """
        key_len = cmap["key length"]
        if key_len not in self.mapping_keys:
            self.mapping_keys[key_len] = \
                [mapped_content[i: i + key_len] for i in range(0, len(mapped_content), key_len)]
        return self.mapping_keys[key_len]
