from abc import abstractclassmethod


class extractor:
    def __init__(self, filename, output):
        self.filename = filename
        self.output = output

    @abstractclassmethod
    def extract_content():
        pass