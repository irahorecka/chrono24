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

## Quick start

Perform a standard search for Rolex DateJust watches:

```python
import chrono24

for listing in chrono24.query("Rolex DateJust").search():
    print(listing)
```

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

Search for standard or detailed watch listings for any query, limiting results to, for example, 25 listings. All results will be retrieved if no limit is provided, and they'll be sorted by new.

```python
import chrono24

rolex_dj = chrono24.query("Rolex DateJust")

# Search for standard listings
for listing in rolex_dj.search(limit=25):
    print(listing)

# Search for detailed listings
for detailed_listing in rolex_dj.search_detail(limit=25):
    print(detailed_listing)
```

**Note:** When using these functions, be cautious not to overwhelm Chrono24 with excessive requests. The `search` method consumes 1 request per 120 posts retrieved, while `search_detail` utilizes 1 request per individual post. Avoid flooding requests to maintain a balanced usage of the Chrono24 service and prevent any potential access limitations.

## API outputs

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

Example output from `.search_detail`, which extends results from `.search`:

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

**Note:** Output keys in `.search` will always be constant, but `.search_detail` can vary based on information provided by the listing page, expanding on the details retrieved by `.search`.

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
