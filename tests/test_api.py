"""
tests/test_api
~~~~~~~~~~~~~~
"""

from functools import reduce

from pytest import mark

import chrono24

# Fetch listings up-front to avoid flooding Chrono24 with requests
ROLEX_DJ = chrono24.query("Rolex DateJust")
DEFAULT_QUERY = chrono24.query("")  # Query with an empty string to test default behavior
SEARCH_LIMIT = 3

# Perform initial searches for listings and detailed listings
LISTINGS = list(ROLEX_DJ.search(limit=SEARCH_LIMIT))
DETAILED_LISTINGS = list(ROLEX_DJ.detailed_search(limit=SEARCH_LIMIT))

# Group standard and detailed listings for parameterized tests
JOINED_LISTINGS = (LISTINGS, DETAILED_LISTINGS)
LISTING = LISTINGS[0]
DETAILED_LISTING = DETAILED_LISTINGS[0]
JOINED_LISTING = (LISTING, DETAILED_LISTING)

# Define the expected standard listing keys for comparison
STANDARD_LISTING_KEYS = {
    "id",
    "url",
    "manufacturer",
    "certification_status",
    "title",
    "description",
    "price",
    "shipping_price",
    "location",
    "merchant_name",
    "badge",
    "image_urls",
}


def test_attrs():
    """Test for checking attributes of the Chrono24 query object."""
    assert isinstance(ROLEX_DJ.count, int), "Count should be an integer."
    assert isinstance(ROLEX_DJ.url, str), "URL should be a string."
    assert isinstance(DEFAULT_QUERY.count, int), "Count should be an integer for default query."
    assert isinstance(DEFAULT_QUERY.url, str), "URL should be a string for default query."


@mark.parametrize("listings", JOINED_LISTINGS)
def test_search_limit_reached(listings):
    """Test to ensure that the search limit is respected."""
    assert len(listings) == SEARCH_LIMIT, f"Expected {SEARCH_LIMIT} listings, got {len(listings)}."


def test_large_search_limit_reached():
    """Test for checking a larger search limit."""
    # Only check standard listings to avoid flooding Chrono24 with too many requests
    limit = 150
    listings = list(ROLEX_DJ.search(limit=limit))
    assert len(listings) == limit, f"Expected {limit} listings, got {len(listings)}."


def test_standard_listing_keys():
    """Ensure that a standard listing dictionary contains only the expected keys."""
    assert len(STANDARD_LISTING_KEYS.union(LISTING.keys())) == len(
        STANDARD_LISTING_KEYS
    ), "Standard listing keys do not match the expected keys."
    assert len(STANDARD_LISTING_KEYS.intersection(LISTING.keys())) == len(
        STANDARD_LISTING_KEYS
    ), "Standard listing keys do not match the expected keys."


def test_detailed_listing_keys():
    """Ensure that detailed listings have more keys than standard listings."""
    assert len(DETAILED_LISTING.keys()) > len(
        STANDARD_LISTING_KEYS
    ), "Detailed listings should have more keys than standard listings."


@mark.parametrize("listing", JOINED_LISTING)
def test_listing_values_are_str_or_list(listing):
    """Ensure that values in a listing are of types `str` or `list` and contain strings."""
    listing_value_types = set(map(lambda x: type(x), listing.values()))
    num_listing_value_types = len(listing_value_types)
    # Assert that only two types (str and list) are in the listing values
    assert (
        num_listing_value_types == 2
    ), "Listing values should only contain `str` and `list` types."
    assert set(listing_value_types).issubset(
        {str, list}
    ), "Listing values should be `str` or `list`."

    # Ensure values inside lists are of type `str`
    list_values = [v for v in listing.values() if isinstance(v, list)]
    if list_values:
        reduced_list_values = reduce(lambda x, y: set(x).union(y), list_values)
        types_list_values = {type(v) for v in reduced_list_values}
        assert (
            len(types_list_values) == 1 and str in types_list_values
        ), "All items inside list values should be of type `str`."


@mark.parametrize("listing", JOINED_LISTING)
def test_listing_keys_are_lowercase(listing):
    """Ensure that all keys in a joined listing are in lowercase."""
    orig_keys = set(listing.keys())
    lowered_keys = set(key.lower() for key in orig_keys)
    assert orig_keys == lowered_keys, "All keys in the listing should be lowercase."


def test_listing_count_matches_search_limit():
    """Test that the total number of listings matches the expected search limit."""
    total_listings = len(LISTINGS) + len(DETAILED_LISTINGS)
    assert (
        total_listings == 2 * SEARCH_LIMIT
    ), f"Expected {2 * SEARCH_LIMIT} total listings, got {total_listings}."


def test_invalid_search_query():
    """Test searching with an invalid query and expect a NoListingsFoundException."""
    try:
        chrono24.query("NonExistentModel12345")
    except chrono24.exceptions.NoListingsFoundException:
        pass  # Expected exception, pass the test
    else:
        raise AssertionError("Expected NoListingsFoundException was not raised.")


def test_listing_urls_are_valid():
    """Ensure that all listing URLs are valid and start with the base URL."""
    base_url = "https://chrono24.com"
    for listing in LISTINGS:
        assert listing["url"].startswith(base_url), f"Listing URL does not start with {base_url}."


def test_merchant_info_in_detailed_listings():
    """Check that merchant information is present in detailed listings."""
    merchant_info_keys = {"merchant_name", "merchant_rating", "merchant_reviews"}
    for key in merchant_info_keys:
        assert key in DETAILED_LISTING, f"Missing merchant info key '{key}' in detailed listing."
        assert isinstance(
            DETAILED_LISTING[key], str
        ), f"Merchant info key '{key}' should be a string."


def test_detailed_listing_contains_additional_keys():
    """Verify that detailed listings contain additional keys not present in standard listings."""
    additional_keys = set(DETAILED_LISTING.keys()) - STANDARD_LISTING_KEYS
    assert len(additional_keys) > 0, "Detailed listings should contain additional keys."
    # Check for specific additional keys that should be present
    expected_additional_keys = {"availabe_payments", "anticipated_delivery", "merchant_badges"}
    assert expected_additional_keys.issubset(
        additional_keys
    ), "Expected additional keys missing from detailed listing."


def test_empty_query():
    """Test querying with an empty string and expect the default behavior."""
    assert DEFAULT_QUERY.count > 0, "Expected non-zero count for default 'used' query."
    assert "usedOrNew=used" in DEFAULT_QUERY.url, "Expected 'used' filter in the default query URL."


def test_filters_show_output(capsys):
    """Test that chrono24.filters.show() displays all filter categories correctly."""
    chrono24.filters.show()
    captured = capsys.readouterr()
    assert (
        "Total number of categories:" in captured.out
    ), "Expected category count in show() output."
    assert "Case" in captured.out, "Expected 'Case' category in show() output."
    assert (
        "Movement and Functions" in captured.out
    ), "Expected 'Movement and Functions' category in show() output."


def test_filters_search_output(capsys):
    """Test that chrono24.filters.search('steel') returns expected filter keys."""
    chrono24.filters.search("steel")
    captured = capsys.readouterr()
    assert (
        "Direct matches:" in captured.out
    ), "Expected 'Direct matches' section in search() output."
    assert "steel_band" in captured.out, "Expected 'steel_band' in search() direct matches."
    assert "Fuzzy matches:" in captured.out, "Expected 'Fuzzy matches' section in search() output."
    assert "gold_steel" in captured.out, "Expected 'gold_steel' in search() fuzzy matches."
