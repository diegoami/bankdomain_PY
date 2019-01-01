
import argparse
import logging
import os
import yaml
import traceback


from crawl import extract_source_without_www, build_links, get_next_available_file, save_links_to_file
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--out_dir')
    args = parser.parse_args()
    site_file =  os.path.join(args.out_dir, 'urls.yml')
    url_processed_file = os.path.join(args.out_dir, 'urls_out.yml')
    qa_dir = os.path.join(args.out_dir, 'qa_urls')

    content = yaml.safe_load(open(site_file ))

    urls_processed = {"urls": {}}
    if os.path.isfile(url_processed_file):
        urls_processed = yaml.safe_load(open(url_processed_file))
    sites = content['sites']
    for site in sites:
        url_host = site["host"]
        dir_to_write = os.path.join(qa_dir, url_host)
        for url in site["urls"]:
            if url not in urls_processed["urls"]:
                logging.info("Processing {}".format(url))
                next_aval_file = get_next_available_file(dir_to_write)
                links = build_links(url=url, block=site["block"], link_selector=site["link_selector"])
                if links:
                    try:
                        save_links_to_file(url=url, file_name=next_aval_file, links=links)
                        url_processed = {"file_name": next_aval_file, "block": site["block"], "link_selector" : site["link_selector"]}
                        urls_processed["urls"][url] = url_processed

                        yaml.safe_dump(urls_processed, open(url_processed_file, 'w'))
                    except:
                        traceback.print_exc()
                        if os.path.isfile(next_aval_file):
                            os.remove(next_aval_file)
                else:
                    logging.info("No links found in url {}...".format(url))
            else:
                logging.info("Skipping ... {}".format(url))
    print(urls_processed)

