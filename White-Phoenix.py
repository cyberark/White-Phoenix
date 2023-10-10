import logging
import os.path
import queue
import concurrent.futures
import sys
import threading
import utils
from extractors.pdf_extractor import PdfExtractor
from extractors.zip_extractor import ZipExtractor
from extractors.vm_extractor import VMExtractor
from identifiers.pdf_identifier import PdfIdentifier
from identifiers.zip_identifier import ZipIdentifier

path_queue = queue.Queue()
lock = threading.Lock()


def delete_folder_contents(folder_path):
    # List all files and directories in the given folder
    folder_contents = os.listdir(folder_path)

    for item in folder_contents:
        item_path = os.path.join(folder_path, item)
        if os.path.isfile(item_path):
            # Delete the file
            os.remove(item_path)
        elif os.path.isdir(item_path):
            # Delete the subdirectory and its contents recursively
            delete_folder_contents(item_path)
            os.rmdir(item_path)


def get_paths(dir):
    if dir:
        return [dir]
    else:
        drives = []
        if os.name == "nt":  # For Windows
            import string
            drives = [d + ":" for d in string.ascii_uppercase if os.path.exists(d + ":")]
        elif os.name == "posix":  # For macOS and Linux
            drives = ["/"]
        return drives


def extract_data_from_file(output, separated_files, file_path, is_vm):
    file_content = utils.read_file(file_path)
    utils.verify_output(output)
    if is_vm:
        extractor = VMExtractor(file_content, output, file_path)
    elif PdfIdentifier(file_content):
        sys.stdout.flush()
        extractor = PdfExtractor(file_content, output, separated_files, file_path)
    elif ZipIdentifier(file_content):
        extractor = ZipExtractor(file_content, output)
    else:
        logging.error("file not supported")
        exit(-1)
    extractor.extract_content()


def find_all_files_path(folder_path, output,vm):
    fifo_queue = queue.Queue()
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                if vm:
                    fifo_queue.put(file_path)
                else:
                    logging.info(f'checking: {file_path}')
                    with open(file_path, "rb") as open_file:
                        content = open_file.read()
                        if PdfIdentifier(content) or ZipExtractor(content, output):
                            fifo_queue.put(file_path)
            except Exception as e:
                logging.error(f'in file:{file_path} - {e}')
    return fifo_queue


def main():
    global path_queue
    if os.path.exists('temp') is not True:
        os.mkdir('temp')
    args = utils.argparse()
    utils.init_logger(args.disable_log)
    if args.filename:
        extract_data_from_file(args.output, args.separated_files, file_path=args.filename, is_vm=args.vm)
    else:
        thread_pool = concurrent.futures.ThreadPoolExecutor(max_workers=10)
        starting_paths = get_paths(args.dir)
        for starting_path in starting_paths:
            temp_queue = find_all_files_path(starting_path, args.output, args.vm)
            while not temp_queue.empty():
                path_queue.put(temp_queue.get())
        while not path_queue.empty():
            lock.acquire()
            file_path = path_queue.get()
            lock.release()
            thread_pool.submit(extract_data_from_file, args.output, args.separated_files, file_path, args.vm)
        thread_pool.shutdown(wait=True)
    delete_folder_contents('temp')


if __name__ == '__main__':
    main()
