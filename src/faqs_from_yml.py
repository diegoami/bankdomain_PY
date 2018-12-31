
import argparse
import logging
import os
import yaml

from crawl import extract_source_without_www, build_qas, get_next_available_file, save_qas_to_file
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--out_dir')
    args = parser.parse_args()
    site_file =  os.path.join(args.out_dir, 'qa.yml')
    url_processed_file = os.path.join(args.out_dir, 'qa_out.yml')
    qa_dir = os.path.join(args.out_dir, 'qa_documents')

    content = yaml.safe_load(open(site_file ))
    sites = content['sites']
    print(content)

    urls_processed = {"urls": {}}
    if os.path.isfile(url_processed_file):
        urls_processed = yaml.safe_load(open(url_processed_file))

    for site in sites:
        url_host = site["host"]
        dir_to_write = os.path.join(qa_dir, url_host)
        for url in site["urls"]:
            if url not in urls_processed["urls"]:
                logging.info("Processing {}".format(url))
                next_aval_file = get_next_available_file(dir_to_write)
                qas = build_qas(url=url, block=site["block"], title=site["title"], text=site["text"])
                if qas:
                    save_qas_to_file(url=url, file_name=next_aval_file, qas=qas)
                    url_processed = {"file_name": next_aval_file, "block": site["block"], "title": site["title"], "text": site["text"]}
                    urls_processed["urls"][url] = url_processed
                else:
                    logging.info("No Q&A found in url {}...".format(url))
            else:
                logging.info("Skipping ... {}".format(url))
    print(urls_processed)
    yaml.safe_dump(urls_processed, open(url_processed_file , 'w'))

