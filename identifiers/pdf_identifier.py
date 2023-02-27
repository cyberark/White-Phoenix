import re

def PdfIdentifier(content):
    """
    Loop through pdf objects to find objects with interesting content
    :return:
    """
    objects_regex = re.compile(b"\D(\d+ 0 obj.*?endobj)", re.S)
    return_object = re.search(objects_regex, content)
    return return_object

