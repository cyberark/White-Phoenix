import pdf_parsers
import utils
from pdf_extractor import pdf_extractor
import logging


def main():
    args = pdf_parsers.argparse()
    utils.init_logger()
    utils.verify_output(args.output)
    file_type = str.lower(args.type)
    if file_type == 'pdf':
        extractor = pdf_extractor(args.filename, args.output)
        extractor.extract_content()
    else:
        logging.error("file Type not supported")



if __name__ == '__main__':
    main()
