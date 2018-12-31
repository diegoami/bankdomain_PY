
import argparse
import logging
import os
import yaml

from crawl import extract_source_without_www, build_qas, get_next_available_file, save_qas_to_file
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--block')
    parser.add_argument('--title')
    parser.add_argument('--text')
    parser.add_argument('--url')
    parser.add_argument('--out_dir')

    args = parser.parse_args()

    url_host = extract_source_without_www(args.url)
    dir_to_write = os.path.join(args.out_dir, 'qa_documents', url_host)
    next_aval_file = get_next_available_file(dir_to_write)
    listing_file = os.path.join(args.out_dir, 'list_out.txt')

    qas = build_qas(url=args.url, block=args.block, title=args.title, text=args.text)
    save_qas_to_file(url=args.url, file_name=next_aval_file, qas=qas)

    with open(listing_file, 'a') as f_lf:
        f_lf.write("{} {} {} {} > {}".format(args.url, args.block, args.title, args.text, next_aval_file))



