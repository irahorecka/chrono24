"""
tests/test_exceptions
~~~~~~~~~~~~~~~~~~~~~
"""
import pytest

import chrono24
from chrono24.exceptions import NoListingsFoundException, RequestException
from chrono24.session import get_response


def test_no_listings_found_exception():
    """Test for NoListingsFoundException."""
    with pytest.raises(NoListingsFoundException):
        list(chrono24("this is an invalid query").search(limit=1))


def test_request_exception():
    """Test for RequestException."""
    with pytest.raises(RequestException):
        invalid_url = "https://irahorecka.com/invalid_endpoint"
        # Only attempt request 3 times
        get_response(invalid_url, max_attempts=3)
