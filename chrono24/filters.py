"""
chrono24/filters
~~~~~~~~~~~~~~~~
"""

import json
from difflib import get_close_matches

from chrono24.constants import (
    case_filters,
    clasp_filters,
    condition_and_delivery_contents_filters,
    dial_filters,
    location_filters,
    movement_and_functions,
    other_filters,
    seller_and_listing_type_filters,
    sort_by_filters,
    strap_bracelet_filters,
    watch_type_filters,
)


class Filters:
    """A class for managing and applying various filters to a collection."""

    # Class-level dictionary that combines all available filter categories
    all_filters = {
        **other_filters,
        **strap_bracelet_filters,
        **clasp_filters,
        **condition_and_delivery_contents_filters,
        **dial_filters,
        **location_filters,
        **movement_and_functions,
        **seller_and_listing_type_filters,
        **watch_type_filters,
        **case_filters,
        **sort_by_filters,  # Most important, added last
    }
    all_filter_keys = sorted(all_filters.keys())

    all_filters_by_category = {
        "Case": case_filters,
        "Clasp": clasp_filters,
        "Condition and Delivery Contents": condition_and_delivery_contents_filters,
        "Dial": dial_filters,
        "Location": location_filters,
        "Movement and Functions": movement_and_functions,
        "Other": other_filters,
        "Seller and Listing Types": seller_and_listing_type_filters,
        "Sort By": sort_by_filters,
        "Strap Bracelet": strap_bracelet_filters,
        "Watch Type": watch_type_filters,
    }

    def __init__(self, to_apply="", min_year=None, max_year=None):
        """Initialize the filter object with optional criteria.

        Args:
            to_apply (str, list, or tuple, optional): Filter criteria to apply during initialization. Can be a single string
                or a collection of filter keys. Default is an empty string. Defaults to "".
            min_year (int, optional): Minimum year for filtering. Defaults to None.
            max_year (int, optional): Maximum year for filtering. Defaults to None.
        """
        self.filters = set()

        # Convert to set based on the type of to_apply
        if isinstance(to_apply, str):
            # Single string is converted to a set with one element
            self.to_apply = {to_apply} if to_apply else set()
        elif isinstance(to_apply, (list, tuple)):
            # List or tuple is converted to a set
            self.to_apply = set(to_apply)
        else:
            raise TypeError(
                f"Invalid type for 'to_apply': {type(to_apply)}. Expected str, list, or tuple."
            )

        self.min_year = min_year
        self.max_year = max_year
        self.apply()

    def __str__(self):
        """Return a string representation of the filters with 4-space indentation.

        Returns:
            str: A JSON-formatted string of the filters list.
        """
        return json.dumps(sorted(self.to_apply), indent=4)

    def apply(self):
        """Apply one or more filters to the current set of filters.

        Raises:
            ValueError: If any of the filter keys are not in `all_filters`.
        """
        if isinstance(self.to_apply, str):
            self.to_apply = set([self.to_apply])

        for filter_key in self.to_apply:
            if filter_key in self.all_filters:
                self.filters.add(self.all_filters[filter_key])
            else:
                filter_suggestions = ", ".join([f"'{s}'" for s in self._fuzzy_match(filter_key)])
                suggestion_message = (
                    f" Did you mean one of these? {filter_suggestions}"
                    if filter_suggestions
                    else ""
                )
                raise ValueError(f"Invalid filter key: '{filter_key}'.{suggestion_message}")

        if not [f for f in self.filters if f.startswith("sortorder=")]:
            self.filters.add("sortorder=5")  # Default sort order is 'Newest listings first'

    @property
    def parameters(self):
        """Get the applied filters as a URL parameter string.

        Returns:
            str: A concatenated string of the applied filters joined by '&'.
        """
        try:
            years = [f"year={y}" for y in range(self.min_year, self.max_year + 1)]
            return "&".join(self.filters) + "&" + "&".join(years)
        except TypeError:
            return "&".join(self.filters)

    @classmethod
    def search(cls, query):
        """Search for matching filter keys based on a given query.

        Args:
            query (str): The query string to search for in the filter keys.

        Returns:
            None: Prints the best matching keys based on the query.
        """
        # Get the best matching keys based on the query
        query = query.lower().replace(" ", "_")  # Normalize the query to match snake_case
        direct_matches = cls._direct_match(query)
        fuzzy_matches = cls._fuzzy_match(query)

        print(f"\nSearch results for query '{query}':\n")
        if direct_matches:
            print("Direct matches:")
            for match in direct_matches:
                print(f"  - {match}")
        else:
            print("No direct matches found.")

        if fuzzy_matches:
            print("\nFuzzy matches:")
            for match in fuzzy_matches:
                print(f"  - {match}")
        else:
            print("No fuzzy matches found.")

        print("")

    @classmethod
    def show(cls):
        """Display all available filters in a JSON-formatted string.

        Returns:
            str: A JSON-formatted string of all available filters.
        """
        num_categories = len(cls.all_filters_by_category)
        print(f"\nTotal number of categories: {num_categories}")
        print(f"\nTotal number of filters: {len(cls.all_filters)}\n")
        for category, filters in cls.all_filters_by_category.items():
            print(category)
            print("=" * len(category))
            for filter_key in sorted(filters.keys()):
                print(f'  - "{filter_key}"')

            print("\n")

    @classmethod
    def _direct_match(cls, query):
        """Search for direct matches based on a given query.

        Args:
            query (str): The query string to search for in the filter keys.

        Returns:
            list: A list of the best matching keys based on the query.
        """
        return [key for key in cls.all_filter_keys if query in key]

    @classmethod
    def _fuzzy_match(cls, query, cutoff=0.5):
        """Search for fuzzy matches based on a given query.

        Args:
            query (str): The query string to search for in the filter keys.
            cutoff (float, optional): The minimum score for a match to be considered.
                Default is 0.5.

        Returns:
            list: A list of the best matching keys based on the query.
        """
        return get_close_matches(query, cls.all_filter_keys, cutoff=cutoff)
