"""
chrono24
~~~~~~~~
"""

import sys

from chrono24.api import chrono24
from chrono24.exceptions import NoListingsFoundException, RequestException


class module_call:
    def __call__(self, query):
        return chrono24(query)


sys.modules[__name__] = module_call()

__version__ = "0.0.1"
