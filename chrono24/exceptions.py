"""
chrono24/exceptions
~~~~~~~~~~~~~~~~~~~
"""


class NoListingsFoundException(Exception):
    """No listings were found."""

    pass


class RequestException(Exception):
    """Repeated requests failed."""

    pass
