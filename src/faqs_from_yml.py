
import argparse
import logging
import os
import yaml
import traceback


from crawl import extract_source_without_www, build_qas, get_next_available_file, save_qas_to_file
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--out_dir')
    args = parser.parse_args()

    noalias_dumper = yaml.dumper.SafeDumper
    noalias_dumper.ignore_aliases = lambda self, data: True
    site_file =  os.path.join(args.out_dir, 'qa.yml')
    url_processed_file = os.path.join(args.out_dir, 'qa_out.yml')
    qa_dir = os.path.join(args.out_dir, 'qa_documents')

    content = yaml.safe_load(open(site_file ))
    print(content)

    urls_processed = {"urls": {}}
    if os.path.isfile(url_processed_file):
        urls_processed = yaml.safe_load(open(url_processed_file))

    sites = content['sites']
    for site in sites:
        for url in site["urls"]:
            if url not in urls_processed["urls"] or not os.path.isfile(urls_processed["urls"][url]["file_name"]):
                dir_to_write = os.path.join(qa_dir, site["host"])

                logging.info("Processing {}".format(url))
                next_aval_file = get_next_available_file(dir_to_write)
                qas = build_qas(url=url, block=site["block"], title=site["title"], texts=site["texts"])
                if qas:
                    try:
                        save_qas_to_file(url=url, file_name=next_aval_file, qas=qas)
                        url_processed = {"file_name": next_aval_file, "block": site["block"], "title": site["title"], "texts": site["texts"]}
                        urls_processed["urls"][url] = url_processed
    #                    yaml.safe_dump(urls_processed, open(url_processed_file, 'w'))
                        with open(url_processed_file, 'w') as dy:
                            dumped_yaml = yaml.dump(urls_processed, default_flow_style=False, Dumper=noalias_dumper)
                            print(dumped_yaml, file=dy)
                    except:
                        traceback.print_exc()
                        if os.path.isfile(next_aval_file):
                            os.remove(next_aval_file)
                else:
                    logging.info("No Q&A found in url {}...".format(url))
            else:
                logging.info("Skipping ... {}".format(url))
    print(urls_processed)

