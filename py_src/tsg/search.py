from tsg.parser import parse_text
from tsg.ranker import rank
from tsg.config import MIN_RESULTS, SPECIFIER_SEPARATOR, FILTER_KEY
import re
import logging

def search(searchphrase, dictionary_path, indexinfo_path):
    """
    Processes a search query and returns a list of matched documents.

    searchphrase: An unformatted search query
    index_directory: The directory where dictionary.dat and indexinfo.json lie.

    IMPORTANT: Use the dictionary.dat path as index_directory parameter
    until the dictionary hash logic is defined.
    """

    field = None
    dict_specifier = 'all'
    if SPECIFIER_SEPARATOR in searchphrase: 
        searchphrase, zone, field = search_filter(searchphrase)

        if field == 'question':
            field = 'faq'

        if zone == FILTER_KEY and field != 'faq' and field != 'doctor':
            dict_specifier = field
            field = None

    print(zone, field)
    dictionary_path = '{}{}{}'.format(dictionary_path, '_', dict_specifier)

    parsed_query = parse_text(searchphrase).split(' ')

    results = rank(parsed_query, dictionary_path, 'and', field)
    if len(results) < MIN_RESULTS:
        results = rank(parsed_query, dictionary_path, 'or', field)

    return results

def search_filter(query):
    field = None
    try:
        zone, field = re.search('([^ ]*{}[^ ]*)'.format(SPECIFIER_SEPARATOR), query).groups()[0].split(SPECIFIER_SEPARATOR) 
    except Exception:
        return query, None, None

    return re.sub('{}{}{}'.format(zone, SPECIFIER_SEPARATOR, field), '', query), zone, field
