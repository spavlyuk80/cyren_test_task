from typing import List

from classes import EmlInstance


def rsearch(obj: dict, key: str):
    """
    Find all occurrences of the key and return value
    """

    # if object is dictionary
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == key:
                yield v
            elif isinstance(v, dict):
                for res in rsearch(v, key):
                    yield res
            elif isinstance(v, list):
                for i in v:
                    for res in rsearch(i, key):
                        yield res

    # just in case it is list of dicts
    elif isinstance(obj, list):
        for i in obj:
            for res in rsearch(i, key):
                yield res


def search_for_keys(msg: EmlInstance, search_keys: List[str]) -> dict:
    """Function that parses the file"""

    parsed_email = msg.parser.decode_email_bytes(msg.raw_email)
    response = {}
    for k in search_keys:
        response[k] = [i for i in rsearch(parsed_email, k)]

    return response
