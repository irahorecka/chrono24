"""
tests/test_exceptions
~~~~~~~~~~~~~~~~~~~~~
"""
import pytest

import chrono24
from chrono24.filters import Filters
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


def test_filters_invalid_key_exception():
    """Test that an invalid filter key raises a ValueError."""
    with pytest.raises(ValueError) as excinfo:
        Filters(to_apply="non_existent_filter").apply()


def test_filters_mixed_invalid_key_exception():
    """Test that a mix of valid and invalid filter keys raises a ValueError."""
    with pytest.raises(ValueError) as excinfo:
        Filters(to_apply=["steel", "invalid_filter_key"]).apply()


def test_filters_none_attribute_error():
    """Test that passing None to Filters causes an AttributeError."""
    with pytest.raises(TypeError):
        filters = Filters(to_apply=None)
        filters.apply()


def test_request_exception_on_invalid_response():
    """Test that RequestException is raised for an invalid HTTP response."""
    with pytest.raises(RequestException):
        invalid_url = "https://chrono24.com/invalid_endpoint"
        get_response(invalid_url, max_attempts=1)  # Reduce attempts for quick failure
