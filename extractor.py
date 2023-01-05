import abc


class Extractor:
    def __init__(self, filename, output):
        self.filename = filename
        self.output = output

    @abc.abstractmethod
    def extract_content(self):
        pass
