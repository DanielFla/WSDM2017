import re
import json
import logging
import os

from lxml import etree

from tsg.config import PARSED_DIR



def extract_content(input_file):
    #Files for FAQ
    main_xpath = '//div[@id="content-body"]'
    title_xpath = '// *[@id = "question-title"]//text()'
    listings_xpath = '//*[@id="question-body"]/text()'

    parser = etree.HTMLParser()
    tree = etree.parse(input_file, parser)
    words = " ".join(tree.xpath(main_xpath))
    listings_count = len(tree.xpath(listings_xpath))
    try:
        title = tree.xpath(title_xpath)[0]
    except IndexError:
        logging.error('File {} doesn\'t seem to have a title'.
                      format(input_file))
        title = ''

    try:
        isbn = tree.xpath('//*[@id="question-body"]/text()')[0]
    except IndexError:
        isbn = ''

    return title, words.replace('\xa0', ' '), isbn, listings_count


def parse_text(unparsed):
    lowered = unparsed.lower().replace('-', ' ')
    parsed = re.sub('[^\w ]', '', lowered)
    parsed = re.sub(' {2,}', ' ', parsed)
    return parsed.strip()


def url_from_filename(input_path):
    base_url = 'https://www.realself.com{}/{}'
    document_type, midpath, endpath = re.match('([^_]*)_([^_]*)_([^\.]*)',
                                               os.path.basename(input_path)).groups()
    if document_type == 'faq':
        return base_url.format('', '{}/{}'.format(midpath, endpath))

    elif document_type == 'doctor':
        return base_url.format('', '{}/{}'.format(midpath, endpath))

    elif document_type == 'conference':
        if midpath != 'conf':
            return base_url.format('db/conf', '{}/{}.html'.format(midpath, endpath))
        else:
            return base_url.format('db/conf', endpath)


def parse_document(document_type, input_path):
    title, words, isbn, listings_count = extract_content(input_path)
    parsed = parse_text(words)
    parsed_title = parse_text(title)
    parsed_url = url_from_filename(input_path)
    uuid = os.path.splitext(os.path.basename(input_path))[0]

    data = {
        'listings_count': listings_count,
        'isbn': isbn,
        'content': parsed,
        'title': parsed_title,
        'url': parsed_url,
        'uuid': uuid,
        'type': document_type
    }
    output_path = '{}{}.json'.format(PARSED_DIR, data['uuid'])
    logging.info('Parsed file {} with uuid {}'.format(input_path, data['uuid']))

    with open(output_path, 'w') as output_file:
        json.dump(data, output_file)
