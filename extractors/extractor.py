import abc


class Extractor:
    def __init__(self, file_content, output):
        self.file_content = file_content
        self.output = output

    @abc.abstractmethod
    def extract_content(self):
        pass
