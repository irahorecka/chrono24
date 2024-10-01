"""
tests/test_filters
~~~~~~~~~~~~~~~~~~
"""

import json

import pytest

from chrono24.filters import Filters

DEFAULT_FILTERS = {"sortorder=5"}


@pytest.fixture
def filters_instance():
    """Fixture to provide a fresh Filters instance for each test."""
    return Filters()


def test_initial_state(filters_instance):
    """Test the initial state of the Filters class."""
    assert filters_instance.filters == DEFAULT_FILTERS


def test_str_method_empty(filters_instance):
    """Test the __str__ method when no filters are applied."""
    assert filters_instance.__str__() == "[]"


def test_apply_single_filter(filters_instance):
    """Test applying a single valid filter key."""
    filters_instance = Filters(to_apply="steel")
    assert len(filters_instance.filters) == 2  # Default sort order and 'steel'


def test_apply_multiple_filters(filters_instance):
    """Test applying multiple valid filters."""
    filters_instance = Filters(to_apply=["steel", "automatic"])
    assert len(filters_instance.filters) == 3  # Default sort order, 'steel', and 'automatic'


def test_apply_invalid_filter_key(filters_instance):
    """Test applying an invalid filter key raises a ValueError."""
    with pytest.raises(ValueError) as excinfo:
        Filters(to_apply="invalid_filter")


def test_apply_mixed_valid_invalid_keys(filters_instance):
    """Test applying a mix of valid and invalid filter keys."""
    with pytest.raises(ValueError) as excinfo:
        filters_instance = Filters(to_apply=["steel", "invalid_filter"])
    assert filters_instance.filters == DEFAULT_FILTERS  # Ensure no valid filters were added


def test_apply_duplicate_filter_key(filters_instance):
    """Test applying the same filter key multiple times does not duplicate entries."""
    filters_instance = Filters(to_apply="steel")
    filters_instance = Filters(to_apply="steel")
    assert len(filters_instance.filters) == 2  # Default sort order and 'steel'


def test_parameters_property(filters_instance):
    """Test the parameters property returns the correct URL parameter string."""
    filters_instance.filters = {"filter1=value1", "filter2=value2"}
    assert filters_instance.parameters in (
        "filter1=value1&filter2=value2",
        "filter2=value2&filter1=value1",
    )


def test_search_and_apply_valid_filters(filters_instance):
    """Test searching and applying filters using valid keys."""
    filters_instance.search("location")
    filters_instance = Filters(to_apply="aluminium_band")
    assert len(filters_instance.filters) == 2  # Default sort order and 'aluminium_band'


def test_str_method_after_applying_filters(filters_instance):
    """Test the __str__ method after applying filters."""
    filters_instance = Filters(to_apply="aluminium_band")
    result = filters_instance.__str__()
    expected_result = json.dumps(["aluminium_band"], indent=4)
    assert result == expected_result


def test_apply_method():
    """Test the application of filters to the Filters object."""
    filters = Filters(to_apply="black_dial")
    filters.apply()
    assert "dialColor=702" in filters.filters, "Black dial filter should be applied."


def test_invalid_filter_key():
    """Test that an invalid filter key raises a ValueError."""
    with pytest.raises(ValueError):
        filters = Filters(to_apply="InvalidFilter")
        filters.apply()


def test_parameters_with_years():
    """Test the parameters property to ensure correct URL parameter generation with year range."""
    filters = Filters(to_apply="steel", min_year=2000, max_year=2002)
    filters.apply()
    params = filters.parameters
    assert "caseMaterials=4" in params, "Expected 'caseMaterials=4' in parameters."
    for i in range(2000, 2003):
        assert f"year={i}" in params, f"Expected 'year={i}' in parameters."


def test_search_method(capsys):
    """Test the search method for direct and fuzzy matches."""
    filters = Filters()
    filters.search("case")
    captured = capsys.readouterr()
    assert "Direct matches:" in captured.out, "Expected direct matches output."
    assert "Fuzzy matches:" in captured.out, "Expected fuzzy matches output."


def test_show_method(capsys):
    """Test the show method output."""
    Filters.show()
    captured = capsys.readouterr()
    assert (
        "Total number of categories" in captured.out
    ), "Expected total number of categories in output."
    assert "Case" in captured.out, "Expected 'Case' category to be displayed."
