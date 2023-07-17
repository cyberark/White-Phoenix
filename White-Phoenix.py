import logging
import utils
from extractors.pdf_extractor import PdfExtractor
from extractors.zip_extractor import ZipExtractor
from identifiers.pdf_identifier import PdfIdentifier
from identifiers.zip_identifier import ZipIdentifier


def main():
    args = utils.argparse()
    utils.init_logger(args.disable_log)
    file_content = utils.read_file(args.filename)
    utils.verify_output(args.output)
    if PdfIdentifier(file_content):
        extractor = PdfExtractor(file_content, args.output, args.separated_files)
    elif ZipIdentifier(file_content):
        extractor = ZipExtractor(file_content, args.output)
    else:
        logging.error("file Type not supported")
        exit(-1)
    extractor.extract_content()


if __name__ == '__main__':
    main()
