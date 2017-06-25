import re
from collections import OrderedDict
from lxml import etree
import os
from os.path import splitext
from tsg.config import RAW_DIR
import operator
import logging


def parse_link(doc_link):
    '''
    Define a function which take a link and obtain the doc_filename string
    and the type of document: journal, conference or author.
    '''
    link_parts = list(re.search('([^/]*)/([^/]*)$', doc_link).groups())

    #if "#" in link_parts[1]:
    #    link_parts[1] = link_parts[1].split("#")[0]

    if "/find/" in doc_link:
        category = "doctor"
    elif "/question/" in doc_link:
        category = "faq"
    else:
        category = "other"

    doc_filename = '{}_{}_{}{}'.format(category,
                                       link_parts[0],
                                       link_parts[1],
                                       '.html')

    return doc_filename

def get_page_outlinks(doc_path):
    xpath_string = "//a[contains(@href, 'find')]/@href" #doctors
    xpath_string2 = "//a[contains(@href, 'question')]/@href"#faq
    parser = etree.HTMLParser()
    page_outlinks = []
    page_outfiles = []

    if os.path.exists(doc_path):
        with open(doc_path) as doc_f:
            tree = etree.parse(doc_f, parser)
            try:
                page_outlinks = tree.xpath(xpath_string) + tree.xpath(xpath_string2)
            except AssertionError:
                os.remove(doc_path)
                return page_outfiles

    for link in page_outlinks:
        page_outfiles.append(parse_link(link))

    return page_outfiles

def build_link_database(html_files_path=RAW_DIR):
    logging.info('Start building link database')
    log_cnt = 0
    doc_dict = {}
    doc_outlinks = {}
    for doc_filename in os.listdir(html_files_path):
        log_cnt += 1
        if log_cnt % 100000 == 0:
            logging.info(
                'Building Link database. Now at file {}'.format(log_cnt))
        if doc_filename.endswith(".html"):
            doc_path = html_files_path + doc_filename
            doc_outlinks[doc_filename] = get_page_outlinks(doc_path)
            for target_doc in doc_outlinks[doc_filename]:
                try:
                    doc_dict[target_doc].append(doc_filename)
                except KeyError:
                    doc_dict[target_doc] = [doc_filename]
        try:
            doc_dict[doc_filename]
        except KeyError:
            doc_dict[doc_filename] = []

    # Unify lists and convert keys to uuid
    doc_dict = {splitext(doc)[0]: [splitext(d)[0] for d in (set(doc_dict[doc]))]
                for doc in doc_dict}

    doc_outlinks = {splitext(doc)[0]: [splitext(d)[0] for d in doc_outlinks[doc]]
                    for doc in doc_outlinks}

    # Sort alphabetically
    ordered_db = OrderedDict(sorted(doc_dict.items(), key=lambda t: t[0]))



    logging.info('Finished building link database')

    return ordered_db, doc_outlinks


def calc_page_rank(html_files_path=RAW_DIR):
    logging.info('Starting calc_page_rank')

    d = 0.85  # Damping in PageRank Algorithm
    threshold = 0.0001  # 1x 10^-3
    iteration_flag = True  # Keep page rank iteration until threshold is met
    log_cnt = 0

    docs_links_db, doc_outlinks = build_link_database(html_files_path)

    pagerank_per_doc = {doc: 1.0 for doc in docs_links_db}

    while iteration_flag:
        log_cnt = 0
        logging.info('Starting new iteration in calculating the page rank')
        tmp_pagerank_per_doc = {}
        for doc, doc_inlinks in docs_links_db.items():
            tmp_pagerank_per_doc[doc] = (1 - d)
            for inlink in doc_inlinks:
                num_outlinks_per_inlink = 0
                if inlink in doc_outlinks:
                    num_outlinks_per_inlink = len(doc_outlinks[inlink])
                    tmp_pagerank_per_doc[doc] += \
                        d * (pagerank_per_doc[inlink] /
                                num_outlinks_per_inlink)
                else:
                    tmp_pagerank_per_doc[doc] = 0

            log_cnt += 1
            if log_cnt % 100000 == 0:
                logging.info('at doc_link {}'.format(log_cnt))

        logging.info('Now investigating stop condition for caculating the'
                     'page rank')

        iteration_flag = False
        for doc in tmp_pagerank_per_doc:
            if (pagerank_per_doc[doc] - tmp_pagerank_per_doc[doc] > threshold):
                iteration_flag = True

        pagerank_per_doc = tmp_pagerank_per_doc

    sorted_pagerank_per_docs = OrderedDict(sorted(pagerank_per_doc.items(),
                                                  key=operator.itemgetter(1, 0),
                                                  reverse=True))

    return sorted_pagerank_per_docs
