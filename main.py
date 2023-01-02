import parsers
import utils
import extractors


def main():
    args = parsers.argparse()
    utils.verify_output(args.output)
    utils.init_logger()
    pdf_objects = parsers.parse_to_objects(args.filename)
    extractors.extract_content(pdf_objects, args.output)


if __name__ == '__main__':
    main()
