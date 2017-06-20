from tsg.parser import parse_text
from tsg.ranker import rank
from tsg.config import MIN_RESULTS

def search(searchphrase, dictionary_path, indexinfo_path):
    """
    Processes a search query and returns a list of matched documents.

    searchphrase: An unformatted search query
    index_directory: The directory where dictionary.dat and indexinfo.json lie.

    IMPORTANT: Use the dictionary.dat path as index_directory parameter
    until the dictionary hash logic is defined.
    """

    parsed_query = parse_text(searchphrase).split(' ')



    results = rank(parsed_query, dictionary_path, 'and')
    if len(results) < MIN_RESULTS:
        results = rank(parsed_query,
                       dictionary_path,
                       'or')

    return results
