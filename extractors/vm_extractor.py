import logging
import re
from extractors.extractor import Extractor
import threading




class VMExtractor(Extractor):
    def __init__(self, file_content, output, file_path):
        super().__init__(file_content, output)
        self.files_dict=dict()
        self.initialize_supported_files_dict()

    def initialize_supported_files_dict(self):
          self.files_dict["pdf"] = rb"%PDF-1\.\d" , rb"%EOF\s{,2}\0+"
          self.files_dict["ooxml"] = rb"PK\x03\x04" , rb"PK\x05\x06.{20}\0"

    def write_file(self,file_type, file_content, i):

        if file_type == "ooxml":
            if b"word/" in file_content[-2000:]:
                file_type = "docx"
            elif b"xl/" in file_content[-2000:]:
                file_type = "xlsx"
            elif b"ppt/" in file_content[-2000:]:
                file_type = "pptx"
            else:
                logging.info("File is not office. Skipping")
                return

        output_name = self.output + "/" + str(hex(threading.current_thread().ident)) + "_" + str(i)+f".{file_type}"
        logging.info(f"writing {output_name}")
        with open(output_name,"wb") as out:
            out.write(file_content)

    def extract_content(self):
        """
        extract all intetesting content from zip or ziplike format
        """
        for file_type in self.files_dict:
                i=0
                logging.info(f"Searching for files of type {file_type}")
                start_addr = 0
                old_addr = 0
                while start_addr != -1:
                        file_match = re.search(self.files_dict[file_type][0],self.file_content[old_addr:])
                        start_addr = file_match.start() if file_match is not None else -1
                        if start_addr != -1:
                                logging.info(f"found file at {hex(start_addr + old_addr)}")
                                file_match = re.search(self.files_dict[file_type][1],self.file_content[old_addr + start_addr:])
                                if file_match is not None:
                                       end_addr = file_match.end()
                                       logging.info(f"found file end at {hex(old_addr + start_addr + end_addr)}")
                                else:
                                       logging.info(f"didn't find file end")
                                       break
                                self.write_file(file_type, self.file_content[start_addr + old_addr:end_addr + old_addr + start_addr], i)

                                i+=1
                                old_addr += start_addr + end_addr
