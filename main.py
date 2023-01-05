import utils
from pdf_extractor import PdfExtractor
from zip_extractor import ZipExtractor


def main():
    args = utils.argparse()
    utils.init_logger()
    utils.verify_output(args.output)
    file_type = str.lower(args.type)
    utils.supported_file_type(file_type)

    if file_type == 'pdf':
        extractor = PdfExtractor(args.filename, args.output)
    else:
        extractor = ZipExtractor(args.filename, args.output)
    extractor.extract_content()


if __name__ == '__main__':
    main()
