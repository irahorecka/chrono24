"""
chrono24
~~~~~~~~
"""

import sys

from chrono24.api import chrono24
from chrono24.exceptions import NoListingsFoundException, RequestException


class Chrono24ModuleCall:
    """A class designed to provide a callable interface for accessing the chrono24 module."""

    def __call__(self, query):
        """Call method to execute the Chrono24ModuleCall class instance as a function.

        Args:
            query (str): A string representing the query to be passed to chrono24.

        Returns:
            chrono24: An object or result returned by the chrono24 instance.
        """
        return chrono24(query)


sys.modules[__name__] = Chrono24ModuleCall()

__version__ = "0.1.0"
