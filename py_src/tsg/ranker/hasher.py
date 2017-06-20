def hash_index_terms(filepath):
    index_terms = {}
    with open(filepath) as index_dict:
        while True:
            pos = index_dict.tell()
            try:
                term, docs = index_dict.readline().split(' ')
            except ValueError:  # nothing left to split: EOF
                break
            else:
                num_docs = len(docs.split(','))

                index_terms[term] = (pos, num_docs)

    return index_terms
