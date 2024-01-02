"""
tests/test_api
~~~~~~~~~~~~~~
"""

from functools import reduce

from pytest import mark

import chrono24


# fmt: off
# Fetch listings up-front to avoid flooding Chrono24 with requests
ROLEX_DJ = chrono24.query("Rolex DateJust")
SEARCH_LIMIT = 3
LISTINGS = list(ROLEX_DJ.search(limit=SEARCH_LIMIT))
DETAILED_LISTINGS = list(ROLEX_DJ.search_detail(limit=SEARCH_LIMIT))
JOINED_LISTINGS = (LISTINGS, DETAILED_LISTINGS)
LISTING = LISTINGS[0]
DETAILED_LISTING = DETAILED_LISTINGS[0]
JOINED_LISTING = (LISTING, DETAILED_LISTING)
STANDARD_LISTING_KEYS = {
    'id', 'url', 'manufacturer', 'certification_status',
    'title', 'description', 'price', 'shipping_price',
    'location', 'merchant_name', 'badge', 'image_urls',
}
# fmt: on


def test_attrs():
    """Test for checking attributes."""
    assert isinstance(ROLEX_DJ.count, int)
    assert isinstance(ROLEX_DJ.url, str)


@mark.parametrize("listings", JOINED_LISTINGS)
def test_search_limit_reached(listings):
    """Test for checking search limit."""
    assert len(listings) == SEARCH_LIMIT


def test_large_search_limit_reached():
    """Test for checking large search limit."""
    # Only check standard listings to avoid flooding Chrono24 with requests
    limit = 150
    listings = list(ROLEX_DJ.search(limit=limit))
    assert len(listings) == limit


def test_standard_listing_keys():
    """Ensure that the retrieved listing dictionary contains only the expected keys."""
    assert len(STANDARD_LISTING_KEYS.union(LISTING.keys())) == len(STANDARD_LISTING_KEYS)
    assert len(STANDARD_LISTING_KEYS.intersection(LISTING.keys())) == len(STANDARD_LISTING_KEYS)


def test_detailed_listing_keys():
    """Ensure that detailed search results have more keys than standard search results."""
    assert len(DETAILED_LISTING.keys()) > len(STANDARD_LISTING_KEYS)


@mark.parametrize("listing", JOINED_LISTING)
def test_listing_values_are_str(listing):
    """Ensure that values in a listing are of types `str` or `list` and contain strings."""
    listing_value_types = set(map(lambda x: type(x), listing.values()))
    num_listing_value_types = len(listing_value_types)
    # Assert only two types in listing values
    assert num_listing_value_types == 2
    # Assert the two value types are list and str
    assert len(set(listing_value_types.union((list, str)))) == num_listing_value_types
    # Assert values inside listing values are of type str
    list_values = [v for v in listing.values() if isinstance(v, list)]
    reduced_list_values = reduce(lambda x, y: set(x).union(y), list_values)
    types_list_values = {type(v) for v in reduced_list_values}
    assert len(types_list_values) == 1


@mark.parametrize("listing", JOINED_LISTING)
def test_listing_keys_are_lower(listing):
    """Ensure that all keys in a joined listing are in lowercase."""
    orig_keys = set(listing.keys())
    lowered_keys = map(lambda x: x.lower(), orig_keys)
    assert len(orig_keys.union(lowered_keys)) == len(orig_keys)
