import json
import os
import logging

from tsg.config import PARSED_DIR, INTERMEDIATE_DIR, FIELDS, CSV_HEADER


def process_document(filepath):
    # read file
    wordlist = {}
    with open(filepath) as f:
        parsed = json.load(f)

    for field in FIELDS:
        for term in parsed[field].split(' '):
            if term == '':
                continue
            try:
                wordlist[term][field] += 1
            except KeyError:
                wordlist[term] = {}
                for field2 in FIELDS:
                    wordlist[term][field2] = 0
                wordlist[term][field] += 1

    return [(term, occurrences) for term, occurrences in wordlist.items()]


def generate_intermediate(file_uuid):
    '''
    filename is same as uuid
    '''
    #logging.info('Indexing file {}'.format(file_uuid))

    wordlist = process_document('{}{}.json'.format(PARSED_DIR, file_uuid))

    for term, occurrences in wordlist:
        term_filename = '{}{}.csv'.format(INTERMEDIATE_DIR, term)
        needs_header = not os.path.isfile(term_filename)

        try:
            with open(term_filename, 'a') as f:
                if needs_header:
                    #logging.info('Creating new index file {}'.format(term_filename))
                    f.write(CSV_HEADER+'\n')

                csv_line = '{},{}\n'.format(
                    file_uuid,
                    ','.join([str(occurrences[field]) for field in FIELDS]))

                f.write(csv_line)
        except OSError as e:
            logging.info('Skipping file {}: {}'.format(term_filename, e))
            pass
