import abc


class Extractor:
    def __init__(self, file_content, output, filename=None):
        self.file_content = file_content
        self.output = output
        self.filename = filename

    @abc.abstractmethod
    def extract_content(self):
        pass
