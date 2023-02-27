import logging
import zipfile
import os
from extractors.extractor import Extractor


class ZipExtractor(Extractor):
    def __init__(self, file_content, output):
        super().__init__(file_content, output)

    def extract_content(self):
        """
        extract all intetesting content from zip or ziplike format
        """
        self.create_temp_file()
        self.extract_files_from_temp()
        self.delete_temp_file()

    def create_temp_file(self):
        """
        create a temporary file that can be parsed by zipfile
        """
        tmp = self.file_content[self.file_content.find(b"PK\x03\x04"):]
        logging.info("Creating temp file in output folder")
        with open(self.output + "/tmp", "wb") as f:
            f.write(tmp)

    def extract_files_from_temp(self):
        """
        extract files from the temp file
        """
        z = zipfile.ZipFile(self.output + "/tmp")
        for entry in z.filelist:
            try:
                z.extract(member=entry, path=self.output)
                logging.info(f"Susscessully extracted {entry.filename} from tmp file")
            except:
                pass

    def delete_temp_file(self):
        """
        remove temp file
        """
        logging.info(f"Deleting temp file")
        os.remove(self.output + "/tmp")