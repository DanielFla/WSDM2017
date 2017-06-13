import re
from tsg.config import THROTTLE_SECONDS


def parse_robots(file_content):
    allowed_list, disallowed_list = ([], [])
    delay = THROTTLE_SECONDS

    for line in file_content.split('\n'):
        matched = re.match('crawl-delay:\s+(.*)', line)
        if matched:
            delay = int(matched.groups()[0])

        matched = re.match('Disallow:\s+(.*)', line)
        if matched:
            disallowed_list.append(matched.groups()[0])

        matched = re.match('Allow:\s+(.*)', line)
        if matched:
            allowed_list.append(matched.groups()[0])

    return delay, allowed_list, disallowed_list
