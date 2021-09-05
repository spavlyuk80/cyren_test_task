import argparse
import os
from typing import List
from loguru import logger
import email
import requests
from pprint import pprint as pp
from lxml.html import fromstring

from classes import EmlInstance
from errors import EmlFileNotFound
from tasks import parse_and_extract, check_authentication, \
    extract_and_get_some_urls_and_count_parse
from utils import search_for_keys


def run_task(**kwargs) -> None:
    """
    runs the task and prints the results

    :param kwargs: any
    :return: None
    """

    # get the path to eml and search keys
    fpath: str = kwargs.get('fpath')
    search_keys: List[str] = kwargs.get('search_keys')

    # init eml class
    msg = EmlInstance()
    # load message
    msg.load_message(fpath)

    # run the tasks
    parse_and_extract(msg=msg, search_keys=search_keys)
    check_authentication(msg=msg)
    extract_and_get_some_urls_and_count_parse(msg=msg)


if __name__ == "__main__":

    # cli args parser
    parser = argparse.ArgumentParser(
        description="This function searches an eml"
                    " message for keys and returns "
                    "their values. If no keys supplied,"
                    "defaults to ['from', 'to', 'message-id']"
    )
    parser.add_argument("-p", type=str, dest="path", help="path to eml file")
    parser.add_argument("-k", type=str, dest="search_keys", nargs="+",
                        help="keys to search in the message")
    args = parser.parse_args()
    default_path = 'test-mail.eml'
    if args.path is None:
        args.path = default_path
    # ensure file exists
    if not os.path.exists(args.path):
        raise EmlFileNotFound("Could not find eml file to parse")

    default_keys = ['from', 'to', 'message-id']

    if args.search_keys is None:
        args.search_keys = default_keys

    run_task(fpath=args.path, search_keys=args.search_keys)
