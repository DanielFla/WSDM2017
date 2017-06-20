''' Calculate quality score for all documents :)'''
import json
import glob
import logging
import numpy as np
from scipy import stats
from tsg.config import CATEGORIES

def get_scores(parsed_directory):
    # read all documents, get a distribution for q scores
    counts = {cat: [] for cat in CATEGORIES}
    doc_counts = {}

    log_cnt = 0
    logging.info('Start scanning documents for qscore.')

    for filename in glob.glob(parsed_directory + '/*.json'):
        with open(filename) as f:
            parsed = json.load(f)
            cat = parsed['type']

            counts[cat].append(parsed['listings_count'])
            doc_counts[parsed['uuid']] = (parsed['listings_count'], cat)

        if log_cnt % 100000 == 0:
            logging.info('Scanned documents for qscore: {}'.format(log_cnt))
        log_cnt += 1

    logging.info('Finished scanning documents. Calculate qscores now')

    distributions = {cat: (np.array(counts[cat]).mean(),
                           np.array(counts[cat]).std()) for cat in CATEGORIES}

    log_cnt = 0

    for key in doc_counts:
        count, cat = doc_counts[key]
        doc_counts[key] = _normalized_quality_score(distributions[cat][0],
                                                    distributions[cat][1],
                                                    count)
        if log_cnt % 100000 == 0:
            logging.info('Calculated Qscore for {} keys'.format(log_cnt))
        log_cnt += 1

    return doc_counts


def _normalized_quality_score(mean, std, listings_count):
    if std == 0:
        p = int(listings_count > mean)
    else:
        p = stats.norm.cdf(listings_count, loc=mean, scale=std)
    return (p+2)/3
