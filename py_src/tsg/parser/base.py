import re
import json
import logging
import os

from lxml import etree

from tsg.config import PARSED_DIR



def extract_content(input_file):
    #Files for FAQ
    main_xpath = '//div[@class="content-body"]//text()'
    title_xpath = '//meta[@property="og:title"]/@content' #question or doctors name
    heading_xpath = '//*[@class="content-title"]/text()' #answer titles or review titles  
    text_xpath = '//div[contains(@class, "original")]//*[@class="content-body-text" or @class="content-body-text user-generated-content"]//text()|//p[@class="content-body-text"]//text()' #answer text or review text
    rating_xpath = '//meta[contains(@content, "UserLikes")]/@content'
    listings_xpath = '//h3[@class="content-title"]//text()' #number of answers or reviews

    parser = etree.HTMLParser()
    tree = etree.parse(input_file, parser)
    parsed_zones = {}
    
    if not tree.getroot():
        logging.error('File {} seems to be empty'.format(input_file))
        raise AssertionError

    parsed_zones['title'] = tree.xpath(title_xpath)[0]
    parsed_zones['words'] = " ".join(tree.xpath(main_xpath))
    parsed_zones['heading'] = ' '.join(tree.xpath(heading_xpath)[1:])
    parsed_zones['text'] = ' '.join(tree.xpath(text_xpath))

    for key in parsed_zones:
        parsed_zones[key] = parse_text(parsed_zones[key].replace('\xa0', ' '))

    listings_count = len(tree.xpath(listings_xpath)) / 2

    return parsed_zones, listings_count


def parse_text(unparsed):
    lowered = unparsed.lower().replace('-', ' ')
    parsed = re.sub('[^\w ]', '', lowered)
    parsed = re.sub(' {2,}', ' ', parsed)
    return parsed.strip()


def url_from_filename(input_path):
    base_url = 'https://www.realself.com/{}/{}'
    document_type, midpath, endpath = re.match('([^_]*)_([^_]*)_([^\.]*)',
                                               os.path.basename(input_path)).groups()
    if document_type == 'faq':
        return base_url.format(midpath, endpath)

    elif document_type == 'doctor':
        midpath
        return base_url.format('{}/{}'.format('find', midpath.replace('.', '/')), endpath)

def parse_document(document_type, input_path):
    try:
        parsed_zones, listings_count = extract_content(input_path)
    except AssertionError:
        return

    parsed_url = url_from_filename(input_path)
    uuid = os.path.splitext(os.path.basename(input_path))[0]

    data = {
        'listings_count': listings_count,
        'content': parsed_zones['words'],
        'title': parsed_zones['title'], #doctors name, question
        'heading': parsed_zones['heading'], #answer titles(questions), review titles(doctor)
        'text': parsed_zones['text'], #answer text(questions), review text(doctor)
        'url': parsed_url,
        'uuid': uuid,
        'type': document_type
    }
    output_path = '{}{}.json'.format(PARSED_DIR, data['uuid'])
    logging.info('Parsed file {} with uuid {}'.format(input_path, data['uuid']))

    with open(output_path, 'w') as output_file:
        json.dump(data, output_file)
