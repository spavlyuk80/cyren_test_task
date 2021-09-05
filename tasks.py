import email
from pprint import pprint as pp
import requests
from loguru import logger
from lxml.html import fromstring

from classes import EmlInstance
from utils import search_for_keys


def parse_and_extract(**kwargs) -> None:
    """
    Parse the file and extract the following headers:
        o From
        o To
        o Message-ID
    :param kwargs: msg
    :return: None
    """

    msg: EmlInstance = kwargs.get('msg')
    search_keys = kwargs.get('search_keys')

    result: dict = search_for_keys(msg=msg, search_keys=search_keys)

    #  pretty print task results
    print(" \n" * 5)
    print(">>>>Let's find the search keys<<<<<<")
    print(" \nThis is what I found in the message reg the search keys using "
          "recursive search\n ")
    pp(result)


def check_authentication(**kwargs) -> None:
    """
    Is it SPF / DKIM authenticated mail?
    :param kwargs: msg
    :return: None
    """
    msg: EmlInstance = kwargs.get('msg')
    spf_result = search_for_keys(msg=msg, search_keys=['received-spf'])
    dkim_result = search_for_keys(msg=msg, search_keys=[
        'authentication-results'])

    # pretty print the result
    print(" \n" * 5)
    print(">>>> Let's check whether it is SPF / DKIM authenticated "
          "mail\n")
    print(" \n>>>> SPF authentication in 'received-spf' key, here is what I "
          "have found")
    print(spf_result)
    print(" \nConclusion is: ")
    # TODO: not general enough
    if "fail" in str(spf_result).lower():
        logger.critical(" \nThis message is not SPF authenticated")
    else:
        logger.success(" \nThis message is SPF authenticated")
    print(" \n" * 2)
    print(" \n>>>>> DKIM validation is in 'authentication-results' key, "
          "here is what I have found\n ")
    pp(dkim_result)
    print(" \nConclusion is: ")
    if "dkim=pass" in str(dkim_result).lower():
        logger.success("This message is DKIM validated")
    else:
        logger.critical("This message is NOT DKIM validated")


def extract_and_get_some_urls_and_count_parse(**kwargs) -> None:
    """
    1. Extract the URLs available in the mail body
    2. Download the landing page for one of the URLs and print the page title
    3. Count the word “parse”

    I put these three tasks into one function since I am reusing some data

    :param kwargs:
    """
    msg: EmlInstance = kwargs.get('msg')

    # extract urls
    message = email.message_from_bytes(msg.raw_email)
    body = msg.parser.get_raw_body_text(msg=message)
    only_message = body[1][1]  # TODO: not generic
    # could have used regex, however why I should reinvent the wheel
    urls = msg.parser.get_uri_ondata(only_message)

    # get the title of the first link
    r = requests.get(urls[0])
    tree = fromstring(r.content)
    title = tree.findtext('.//title')

    # count the word parse
    words = only_message.lower().split()

    # pretty print the results
    print(" \n" * 5)
    print(" \n>>>>> Let's extract urls from the message, using eml_parser "
          "module\n ")
    print("Extracted urls are:")
    pp(urls)
    print(" \n" * 5)
    print(">>>>> Let's get the title of the first url")
    print(f"Title is: {title}")
    print(" \n" * 5)
    print(">>>>> Let's get count of word parse in the message")
    print(f"I found {len([i for i in words if i == 'parse'])} occurrences of "
          f"'parse' in the message")

    logger.success("Looks like I am done!")
