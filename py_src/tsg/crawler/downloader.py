import logging
import requests
import time
import datetime
import urllib


from tsg.config import THROTTLE_SECONDS, ALLOWED_SITES, DISALLOWED_SITES


def get_site(url):
    """Crawls site and checks for error. Waits if necessary

    :url: The url to crawl
    :returns: The website object returned by requests.get

    """

    # first check if we are allowed do download the url!
    url_path = urllib.parse.urlparse(url).path
    if len(ALLOWED_SITES) > 0:
        for allowed in ALLOWED_SITES:
            if allowed in url_path:
                break
        else:
            raise ValueError('Illegal URL. Check robots.txt')

    for disallowed in DISALLOWED_SITES:
        if disallowed in url_path:
            raise ValueError('Illegal URL. Check robots.txt')



    while True:
        wait_time = THROTTLE_SECONDS - \
            (datetime.datetime.now().timestamp()-get_site.last_call)
        if wait_time > 0:
            time.sleep(wait_time)
        result = requests.get(url)
        get_site.last_call = datetime.datetime.now().timestamp()

        if result.status_code != 200:
            logging.warn('There was a problem getting URL {}: Status code: {}'.
                         format(url, result.status_code))

            if result.status_code == 404:
                raise result.raise_for_status()

            if result.status_code == 429:
                retry_after = int(result.headers['retry-after'])
                logging.info('Waiting for {} seconds'.format(
                    retry_after
                ))
                print('Waiting now. Press Control+C to go on before the timout')
                try:
                    time.sleep(retry_after)
                except KeyboardInterrupt:
                    pass
        else:
            return result
get_site.last_call = datetime.datetime.now().timestamp()
