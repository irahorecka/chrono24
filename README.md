# chrono24

<p align="center">
  <img src="https://static.chrono24.com/images/default/logo-positive-reduced.svg" width="50%" />
</p>

<br>

[Chrono24](https://www.chrono24.com/) API wrapper

[![pypiv](https://img.shields.io/pypi/v/chrono24.svg)](https://pypi.python.org/pypi/chrono24)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![continuous-integration](https://github.com/irahorecka/chrono24/workflows/continuous-integration/badge.svg)](https://github.com/irahorecka/chrono24/actions)
[![Licence](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/irahorecka/chrono24/main/LICENSE)

## Installation

```bash
pip install chrono24
```

## Quick Start

Perform a standard search for Rolex DateJust watches:

```python
import chrono24

for listing in chrono24.query("Rolex DateJust").search():
    print(listing)
```

Example output:

```python
>>> {'id': '32322343',
    'url': 'https://chrono24.com/rolex/datejust-41mm-blue-diamond-dial-2022---126334--id32322343.htm',
    'manufacturer': 'Rolex',
    'certification_status': 'Basic',
    'title': 'Rolex Datejust 41',
    'description': '41mm Blue Diamond Dial 2022 - 126334',
    'price': '$16,553',
    'shipping_price': '$396',
    'location': 'Düsseldorf, Germany.',
    'merchant_name': 'Dealer',
    'badge': 'Professional',
    'image_urls': ['https://cdn2.chrono24.com/images/uhren/32322343-gp8hzm4ppkzsbhzc7s7bl2vh-ExtraLarge.jpg',
    'https://cdn2.chrono24.com/images/uhren/32322343-u7wq78hxqoalnfrlag1gkt8d-ExtraLarge.jpg',
    'https://cdn2.chrono24.com/images/uhren/32322343-93ykurb99s654x7aysnh8ljs-ExtraLarge.jpg',
    'https://cdn2.chrono24.com/images/uhren/32322343-gxd85po61ynmoictprm1gvfq-ExtraLarge.jpg',
    'https://cdn2.chrono24.com/images/uhren/32322343-den0sntpacmucq5zdktzul70-ExtraLarge.jpg']}
    # ...
```

## Usage

Search for standard or detailed watch listings for any query, limiting results to, for example, 25 listings. All results will be retrieved if no limit is provided, and they'll be sorted by new listings first.

```python
import chrono24

rolex_dj = chrono24.query("Rolex DateJust")

# Search for standard listings
for listing in rolex_dj.search(limit=25):
    print(listing)

# Search for detailed listings
for detailed_listing in rolex_dj.detailed_search(limit=25):
    print(detailed_listing)
```

**Note:** When using these functions, be cautious not to overwhelm Chrono24 with excessive requests. The `standard_search` method consumes 1 request per 120 posts retrieved, while `detailed_search` utilizes 1 request per individual post. Avoid flooding requests to maintain a balanced usage of the Chrono24 service and prevent any potential access limitations.

## API Outputs

Example output from `.search`:

```python
{
    'id': '32322343',
    'url': 'https://chrono24.com/rolex/datejust-41mm-blue-diamond-dial-2022---126334--id32322343.htm',
    'manufacturer': 'Rolex',
    'certification_status': 'Basic',
    'title': 'Rolex Datejust 41',
    'description': '41mm Blue Diamond Dial 2022 - 126334',
    'price': '$16,553',
    'shipping_price': '$396',
    'location': 'Düsseldorf, Germany.',
    'merchant_name': 'Dealer',
    'badge': 'Professional',
    'image_urls': [...],  # List of image URLs
}
```

Example output from `.detailed_search`, which extends results from `.search`:

```python
{
    'id': '32322343',
    'url': 'https://chrono24.com/rolex/datejust-41mm-blue-diamond-dial-2022---126334--id32322343.htm',
    'manufacturer': 'Rolex',
    'certification_status': 'Basic',
    'title': 'Rolex Datejust 41',
    'description': '41mm Blue Diamond Dial 2022 - 126334',
    'price': '$16,553',
    'shipping_price': '$396',
    'location': 'Düsseldorf, Germany.',
    'merchant_name': 'Dealer',
    'badge': 'Professional',
    'image_urls': [...],  # List of image URLs
    'listing_code': 'J8S2V6',
    'brand': 'Rolex',
    'model': 'Datejust 41',
    'reference_number': '126334',
    'dealer_product_code': '8675310109006',
    'case_material': 'Steel',
    'bracelet_material': 'Steel',
    'year_of_production': '2022',
    'condition': 'Very good (Worn with little to no signs of wear)',
    'scope_of_delivery': 'Original box, original papers',
    'availability': 'Item needs to be procured',
    'case_diameter': '41 mm',
    'bracelet_color': 'Steel',
    'availabe_payments': [...],  # List of available payment methods
    'anticipated_delivery': 'Latest anticipated delivery on 1/22',
    'merchant_rating': '4.4',
    'merchant_reviews': '196',
    'merchant_badges': [...],  # List of merchant badges
}
```

**Note:** Output keys in `.search` will always be constant, but `.detailed_search` can vary based on information provided by the listing page, expanding on the details retrieved by `.search`.

## Filters

You can refine your watch searches using various filter criteria, as well as define year ranges using `min_year` and `max_year`. Pre-defined filters include options such as case material, bracelet type, movement type, and more. These filters and year constraints can be applied when creating a query object.

### How to Use Filters

To use filters, specify them when creating a query using the `filters` argument. You can pass a single string, a list/tuple of filter keys, or include year constraints using the `min_year` and `max_year` parameters:

```python
import chrono24

# Initialize a query with a single filter
steel_rolex_dj = chrono24.query("Rolex DateJust", filters="steel")
# Initialize a query with multiple filters
steel_auto_rolex_dj = chrono24.query("Rolex DateJust", filters=["steel", "automatic"])
# Initialize a query with year constraints
new_rolex_dj = chrono24.query("Rolex DateJust", min_year=2010, max_year=2020)
# Combine filters and year constraints
new_steel_auto_rolex_dj = chrono24.query("Rolex DateJust", filters=["steel", "automatic"], min_year=2010, max_year=2020)
```

### Available Filter Categories

The available filter categories are:

- **Case Filters**: Material, diameter, and more.
- **Clasp Filters**: Clasp type, material, etc.
- **Condition and Delivery Contents**: Item condition, delivery options, included papers/box.
- **Dial Filters**: Dial color, numerals, etc.
- **Location Filters**: Country-specific filters.
- **Movement and Functions**: Manual, automatic, complications.
- **Other Filters**: Miscellaneous filters such as water resistance, glass type.
- **Seller and Listing Type**: Dealer, private seller, new/used.
- **Sort By**: Sorting options like 'Newest listings first', 'Price ascending', etc.
- **Strap and Bracelet**: Bracelet material, color, strap type.
- **Watch Type**: Sports, dress, luxury, and more.

### Finding Filters

You can view all available filters using the `chrono24.filters.show()` method:

```python
import chrono24

# Display all available filter categories and keys
chrono24.filters.show()
```

This will print a categorized list of all possible filters, helping you decide which ones to apply to your query. If you're not sure which filter to use, you can also search for filter keys using the `chrono24.filters.search(query)` method:

```python
import chrono24

# Search for filters related to 'steel'
chrono24.filters.search("steel")
```

Example output:

```text
Search results for query 'steel':

Direct matches:
  - gold_steel_band
  - steel_band
  - gold_steel_color
  - steel_band_color
  - gold_steel_clasp
  - steel_clasp
  - gold_steel
  - steel
  - gold_steel_bezel
  - steel_bezel

Fuzzy matches:
  - steel
  - steel_band
  - gold_steel
  - steel_clasp
  - steel_bezel
```

This output shows the best filter keys matching the query 'steel', divided into **Direct matches** (exact or close matches) and **Fuzzy matches** (similar but not exact matches). Use these filter keys to refine your watch search in `chrono24`.

## Attributes

The `chrono24` instance offers public attributes:

- `count`: Total number of listings found.
- `url`: URL of listings page.

```python
import chrono24

rolex_dj = chrono24.query("Rolex DateJust")

rolex_dj.count
# >>> 35582
rolex_dj.url
# >>> 'https://www.chrono24.com/rolex/datejust--mod45.htm?dosearch=true&query=Rolex+DateJust'
```

## Exceptions

The `chrono24` package handles specific exceptions that might occur during its use:

- `NoListingsFoundException`: Raised when no listings are found.
- `RequestException`: Raised when a request error occurs or repeated requests fail.

```python
import chrono24
from chrono24.exceptions import NoListingsFoundException, RequestException

try:
    invalid_query = chrono24.query("Invalid Query")
except NoListingsFoundException:
    # In cases where no listings match the provided query
    print("No listings were found.")
except RequestException:
    # In cases where a request error occurs or repeated requests fail
    print("Request error or repeated requests failed.")
```

## Contribute

- [Issues Tracker](https://github.com/irahorecka/chrono24/issues)
- [Source Code](https://github.com/irahorecka/chrono24/tree/main/chrono24)

## Support

If you are having issues or would like to propose a new feature, please use the [issues tracker](https://github.com/irahorecka/chrono24/issues).

## License

This project is licensed under the MIT license.
