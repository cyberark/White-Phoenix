import re

def PdfIdentifier(content):
    """
    Sherach for PDF object  
    Return: None, if the item is not found 
    """
    objects_regex = b"\d+ 0 obj."
    return re.search(objects_regex, content)

