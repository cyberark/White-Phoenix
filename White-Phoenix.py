import logging
import utils
from extractors.pdf_extractor import PdfExtractor
from extractors.zip_extractor import ZipExtractor
from identifiers.pdf_identifier import PdfIdentifier
from identifiers.zip_identifier import ZipIdentifier

def identify_content(file_content):
    ans = None  
    if PdfIdentifier(file_content):
        ans = "pdf"
    elif ZipIdentifier(file_content):
        ans = "zip"
    else:
        logging.error("file Type not supported")
        exit(-1)
    return ans
    

def main():
    args = utils.argparse()
    utils.init_logger()

    file_content = utils.read_file(args.filename)
    utils.verify_output(args.output)
    
    file_type = identify_content(file_content)

    if file_type == 'pdf':
        extractor = PdfExtractor(file_content, args.output)
    elif file_type == 'zip':
        extractor = ZipExtractor(file_content, args.output)
    extractor.extract_content()


if __name__ == '__main__':
    main()
