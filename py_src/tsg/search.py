from tsg.parser import parse_text
from tsg.ranker import rank
from tsg.config import MIN_RESULTS, SPECIFIER_SEPARATOR
import re

def search(searchphrase, dictionary_path, indexinfo_path):
    """
    Processes a search query and returns a list of matched documents.

    searchphrase: An unformatted search query
    index_directory: The directory where dictionary.dat and indexinfo.json lie.

    IMPORTANT: Use the dictionary.dat path as index_directory parameter
    until the dictionary hash logic is defined.
    """

    if SPECIFIER_SEPARATOR in searchphrase: 
        searchphrase = search_filter(searchphrase)
    parsed_query = parse_text(searchphrase).split(' ')

    results = rank(parsed_query, dictionary_path, 'and')
    if len(results) < MIN_RESULTS:
        results = rank(parsed_query, dictionary_path, 'or')

    return results

def search_filter(query):
    field, specifier = re.search('([^ ]*:[^ ]*)', query).groups()[0].split(SPECIFIER_SEPARATOR) 

    query = re.sub(SPECIFIER_SEPARATOR.join([field, specifier]), '', query) 
    return query
