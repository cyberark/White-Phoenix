import parsers
import utils
import extractors
import logging


def main():
    args = parsers.argparse()
    utils.init_logger()
    utils.verify_output(args.output)
    file_type = str.lower(args.type)
    if file_type == 'pdf':
        pdf_objects = parsers.parse_to_objects(args.filename)
        extractors.extract_content(pdf_objects, args.output)
    else:
        logging.error("file Type not supported")



if __name__ == '__main__':
    main()
