import utils
from extractors.pdf_extractor import PdfExtractor
from extractors.zip_extractor import ZipExtractor


def main():
    args = utils.argparse()
    utils.init_logger()

    file_content = utils.read_file(args.filename)
    utils.verify_output(args.output)
 
    file_type = str.lower(args.type)
    utils.supported_file_type(file_type)

    if file_type == 'pdf':
        extractor = PdfExtractor(file_content, args.output)
    else:
        extractor = ZipExtractor(file_content, args.output)
    extractor.extract_content()


if __name__ == '__main__':
    main()
