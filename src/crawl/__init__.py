from urllib.parse import urlparse, urlsplit, urljoin

from bs4 import BeautifulSoup
import requests
import os
import logging

def extract_source( url):
    source = str(urlparse(url)[1]).lower()
    return source

def extract_host( url):
    base_url = "{0.scheme}://{0.netloc}/".format(urlsplit(url))
    return base_url



def is_absolute(url):
    return bool(urlparse(url).netloc)

def extract_source_without_www( url):
    try:
        source = extract_source( url).lower()
        all_parts = source.split('.')
        parts = [ x for x in all_parts if x not in ['www'] ]
        return ".".join(parts)
    except:
        return url

def get_next_available_file(dir_to_write):
    os.makedirs(dir_to_write, exist_ok=True)
    file_index = 1
    while True:
        file_out = os.path.join(dir_to_write, "{}.txt".format(file_index))
        if not os.path.isfile(file_out):
            return file_out
        else:
            file_index += 1


def build_qas(url, block, title, texts):
    r = requests.get(url)
    soup = BeautifulSoup(r.content)
    blocks = soup.select(block)

    qas = []
    qa = {}
    for block in blocks:
        for part in block.descendants:
            if part.name == title:
                if qa:
                    qas.append(qa)
                    qa = {}
                qa = {'title': "".join(map(str,part.text))}
            elif part.name in texts and "title" in qa:
                qa['text'] = qa.get('text', "") + "".join(map(str, part.text)) + " "
    if qa:
        qas.append(qa)
    return qas

def build_links(url, block, link_selector):
    r = requests.get(url)
    soup = BeautifulSoup(r.content)
    blocks = soup.select(block)
    host = extract_host(url)
    links = []

    for block in blocks:
        parts = block.select(link_selector)
        for part in parts:
            link = part.attrs["href"]
            if is_absolute(link):
                links.append(link)
            else:
                link = urljoin(host, link)
                links.append(link)
    return links


def save_qas_to_file(url, file_name, qas):
    logging.info("Saving qas: {} to file {}".format(qas, file_name))
    all_lines = ""
    all_lines += "### {}\n".format(url)
    all_lines += "###\n"
    for qa in qas:
        if "text" in qa:
            all_lines += qa["title"]
            all_lines += "\n"
            all_lines += qa["text"]
            all_lines += "\n###\n"
        else:
            logging.info("No answer found for {}".format(qa.get("title", "No title found")))
    with open(file_name, 'w') as f_qas:
        print(all_lines, file=f_qas)


def save_links_to_file(url, file_name, links):
    logging.info("Saving links: {} to file {}".format(links, file_name))
    all_lines = ""
    all_lines += "### {}\n".format(url)
    all_lines += "###\n"
    for link in links:
        all_lines += link
        all_lines += "\n"

    with open(file_name, 'w') as f_links:
        print(all_lines, file=f_links)