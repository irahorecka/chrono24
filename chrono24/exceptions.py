"""
chrono24/exceptions
~~~~~~~~~~~~~~~~~~~
"""


class NoListingsFoundException(Exception):
    """No listings were found."""

    pass


class RequestException(Exception):
    """Invalid request or repeated requests failed."""

    pass
