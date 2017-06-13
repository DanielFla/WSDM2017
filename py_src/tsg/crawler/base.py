from lxml import html
import requests
import re
import os
import logging
import validators
from tsg import config
from tsg.crawler.downloader import get_site
from tsg.robots_parser import parse_robots

def crawl_site(url, category):
    logging.info('Downloading URL site {}'.format(url)) # for instance ['https:', '', 'www.realself.com', 'find', 'Australia', 'Kingswood', 'Plastic-Surgeon', 'Angelo-Preketes']
    url_parts = re.split('/', url)
    filename = '{}_{}_{}{}'.format(category,
                                   url_parts[-2], #for the doctor case to prevent confusion if two doctors with the same name exist
                                   url_parts[-1], #last one: name or question 
                                   '.html')

    doc_path = config.RAW_DIR + filename
    if os.path.isfile(doc_path):
        logging.warn('File {} exists already. Skipping'.format(doc_path))
        return

    try:
        webpage = get_site(url)
        with open(doc_path, 'w') as f:
            f.write(webpage.text)
            logging.info('File at {}'.format(doc_path))
    except requests.exceptions.HTTPError:
        pass

def crawl_urls(url):
    logging.info('Downloading URL {}'.format(url))
    webpage = get_site(url)
    tree = html.fromstring(webpage.content)
    links = tree.xpath("//url/loc/text()")
    return links

def crawl_loop(category, n=0):
    robots_file = get_site(config.SITE_ROBOTS_TXT)
    config.THROTTLE_SECONDS, config.ALLOWED_SITES, config.DISALLOWED_SITES = \
        parse_robots(robots_file.text)

    for i,c in enumerate(config.CATEGORIES):
        if category == c:
            url = config.SITE + config.SITE_CATEGORIES[i]
            pagination = 1
            break
    else:
        raise ValueError('category must be one of ' + config.CATEGORIES + '!')

    while True:
        links = crawl_urls(url.format(str(n)))
        if len(links) < 1:
            logging.warn('Didn\' find any links')
            break
        for link in links:
            crawl_site(link, category)
        n += pagination
    return n
