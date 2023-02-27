import re

def ZipIdentifier(content):
    """
    Loop through pdf objects to find objects with interesting content
    :return:
    """
    objects_regex = re.compile(b"PK\x03\x04", re.S)
    return_object = re.search(objects_regex, content)
    return return_object