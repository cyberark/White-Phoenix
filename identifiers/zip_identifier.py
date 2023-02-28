import re

def ZipIdentifier(content):
    """
    Search for Zip Magic
    Return: None, if the item is not found 
    """
    objects_regex = b"PK\x03\x04"
    return re.search(objects_regex, content)
