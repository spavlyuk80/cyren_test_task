import os
import eml_parser
from errors import EmlFileNotFound


class EmlInstance:
    """
    extends EmlParser to manipulate eml messages
    """
    parser = eml_parser.EmlParser()
    raw_email = None

    def __init__(self, *args, **kwargs):
        pass

    def load_message(self, fpath) -> None:
        """
        Reads email message
        :param fpath: path to eml message
        """
        if os.path.exists(fpath):
            with open(fpath, 'rb') as f:
                self.raw_email = f.read()
        else:
            raise EmlFileNotFound()
