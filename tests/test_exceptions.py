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
        chrono24.query("this is an invalid query")


def test_request_exception():
    """Test for RequestException."""
    with pytest.raises(RequestException):
        invalid_url = "https://irahorecka.com/invalid_endpoint"
        # Only attempt 3 requests
        get_response(invalid_url, max_attempts=3)
