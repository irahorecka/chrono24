"""
chrono24/api
~~~~~~~~~~~~
"""

import re
from functools import lru_cache

from bs4 import BeautifulSoup

from chrono24.exceptions import NoListingsFoundException
from chrono24.session import get_html, get_response

BASE_URL = "https://chrono24.com"
NULL_VALUE = "null"


def get_text_html_tag_or_null(html_tag):
    """Get the text from an HTML tag or return NULL_VALUE if the tag is None or has no text.

    Args:
        html_tag (bs4.element.Tag or None): The HTML tag to extract text from.

    Returns:
        str: The text content of the HTML tag, or NULL_VALUE if the tag is None or has no text.
    """
    html_tag_text = html_tag.text.strip() if html_tag else ""
    return html_tag_text or NULL_VALUE


class chrono24:
    """A class for performing searches on Chrono24."""

    base_query_url = BASE_URL + "/search/index.htm?dosearch=true&query="
    page_size = 120

    def __init__(self, query):
        """
        Initialize a chrono24 object with a query.

        Args:
            query (str): The search query to be performed.
        """
        self.query = query

    def search(self, limit=None):
        """Performs a search using the _search method with an optional limit.

        Args:
            limit (int, optional): An optional integer representing the maximum number of results to return.

        Yields:
            Iterator[dict]: Listings found from search.
        """
        yield from self._search(self._get_standard_listing, limit)

    def search_detail(self, limit=None):
        """Performs a detailed search using the _search method with an optional limit.

        Args:
            limit (int, optional): An optional integer representing the maximum number of detailed results to return.

        Yields:
            Iterator[dict]: Detailed listings found from search.
        """
        yield from self._search(self._get_detailed_listing, limit)

    def _search(self, get_listing, limit):
        """Perform a search and yield individual listings based on the given get_listing function.

        Args:
            get_listing (function): A function to process individual listings.
            limit (int, optional): The maximum number of listings to yield. Defaults to None.

        Yields:
            Listing: A processed listing obtained from the search results.
        """
        # Get HTML content for the first page to find total page count for query
        request_attrs = {
            "pageSize": self.page_size,  # Number of listings per results page
            "showPage": 1,  # What page to view
            "sortorder": 5,  # Sort by newest listings
        }
        listings = self._get_listings(**request_attrs)
        total_page_count = self._get_total_page_count(listings)
        if not total_page_count:
            return
        # Iterate through all pages and yield individual listings as JSON
        num_listings_yielded = 0
        for page_number in range(1, total_page_count + 1):
            # First page of query URL already declared - simply yield its listings
            if page_number != 1:
                request_attrs["showPage"] = page_number
                listings = self._get_listings(**request_attrs)
            for listing in listings:
                if limit and num_listings_yielded >= limit:
                    return
                yield get_listing(listing)
                num_listings_yielded += 1

    def _get_total_page_count(self, listings):
        """Calculate the total number of pages based on the total listing count.

        Args:
            listings (Listings): The listings object used to extract the total listing count.

        Returns:
            int: The total number of pages calculated based on the total listing count.

        Raises:
            NoListingsFoundException: Raised if the query is invalid and unable to retrieve the total listing count.
        """
        try:
            return listings.total_listings_count // self.page_size + 1
        # Unable to get total listing count because of invalid query
        except AttributeError as e:
            raise NoListingsFoundException(f"'{self.query}' is not a valid query.") from e

    def _get_listings(self, **kwargs):
        """Get listings based on the provided keyword arguments.

        Args:
            **kwargs: URL attributes for customizing the query URL.

        Returns:
            Listings: A Listings object containing the fetched listings.
        """
        query_url = self.base_query_url + self.query.replace(" ", "+")
        response_url = get_response(query_url).url + self._join_attrs(**kwargs)
        page_number = kwargs.get("showPage", 1)
        if page_number != 1:
            response_url = response_url.replace("index.htm", f"index-{page_number}.htm")

        return Listings(get_html(response_url))

    def _get_standard_listing(self, listing):
        """Get the standard JSON representation of a listing.

        Args:
            listing (Listing): The listing object to extract JSON representation from.

        Returns:
            dict: The standard JSON representation of the listing.
        """
        return listing.json

    def _get_detailed_listing(self, listing):
        """Get a detailed JSON representation of a listing by combining its standard JSON
        with additional details fetched from its URL.

        Args:
            listing (Listing): The listing object to extract detailed information from.

        Returns:
            dict: The detailed JSON representation of the listing.
        """
        return {**listing.json, **DetailedListing(get_html(listing.json["url"])).json}

    @staticmethod
    def _join_attrs(**kwargs):
        """Join keyword arguments into a URL query string format.

        Args:
            **kwargs: URL attibutes to be joined into a query string.

        Returns:
            str: A string representation of the joined URL query parameters.
        """
        return "&" + "&".join(f"{k}={v}" for k, v in kwargs.items())


class Listings:
    """A class representing a collection of listings extracted from HTML content."""

    def __init__(self, html):
        """
        Initialize the Listings object with HTML content.

        Args:
            html (bs4.element.ResultSet): The HTML content containing listings.
        """
        self.html = html

    def __iter__(self):
        """Iterate through the listings and yield StandardListing objects.

        Yields:
            StandardListing: An object representing a standard listing.

        Raises:
            NoListingsFoundException: Raised when no listings are found in the HTML content.
        """
        listings_div = self.html.find("div", {"id": "wt-watches"})
        if not listings_div:
            raise NoListingsFoundException("No listings were found.")
        listings = listings_div.find_all("a", {"class": "js-article-item"})
        for listing in listings:
            yield StandardListing(listing)

    @property
    def total_listings_count(self):
        """Get the total count of listings from the HTML content.

        Returns:
            int: The total count of listings as an integer.

        Notes:
            If the total count of listings cannot be found or parsed from the HTML content, returns 0.
        """
        re_pattern_comma_sep_num = r"\b\d{1,3}(?:,\d{3})*\b"
        listings_count_text = get_text_html_tag_or_null(
            self.html.find("div", {"class": "h1 m-b-0 m-t-0"})
        )
        match = re.search(re_pattern_comma_sep_num, listings_count_text)
        # Return total listing count as integer, otherwise 0
        return int(match.group().replace(",", "")) if match else 0


class StandardListing:
    """Represents a standard listing extracted from HTML content."""

    def __init__(self, html):
        """Initialize a StandardListing object with HTML content.

        Args:
            html (bs4.element.Tag): The HTML content representing the listing.
        """
        self.html = html

    @property
    @lru_cache(maxsize=64)
    def json(self):
        """Extract JSON representation of the listing from the HTML.

        Returns:
            dict: A dictionary containing the extracted listing information.
        """
        return {
            "id": self.html["data-article-id"].strip(),
            "url": BASE_URL + self.html["href"].strip(),
            "manufacturer": self.html["data-manufacturer"].strip(),
            "certification_status": self.html["data-watch-certification-status"].strip(),
            "title": get_text_html_tag_or_null(
                self.html.find("div", {"class": "text-bold text-ellipsis"})
            ),
            "description": get_text_html_tag_or_null(
                self.html.find("div", {"class": "text-ellipsis m-b-2"})
            ),
            "price": get_text_html_tag_or_null(
                (lambda x: x.parent if x else x)(self.html.find("span", {"class": "currency"}))
            ),
            "shipping_price": self._shipping_price,
            "location": self._location_and_merchant_name[0],
            "merchant_name": self._location_and_merchant_name[1],
            "badge": self._badge,
            "image_urls": self._image_urls,
        }

    @property
    def _shipping_price(self):
        """Get the shipping price from the HTML content.

        Returns:
            str: The shipping price extracted from the content, formatted as a string ('$X' format).
        """
        shipping_price_text = get_text_html_tag_or_null(
            self.html.find("div", {"class": "text-muted text-sm"})
        )
        re_pattern_shipping_cost = r"\b\d{1,3}(?:,\d{3})*\b"
        match = re.search(re_pattern_shipping_cost, shipping_price_text)
        return f'${match.group() if match else "0"}'

    @property
    @lru_cache(maxsize=64)
    def _location_and_merchant_name(self):
        """Get the location and merchant name from the HTML content.

        Returns:
            tuple: A tuple containing the location and merchant name extracted from the content.
        """
        location = self.html.find("button", {"class": "js-tooltip"})["data-content"].strip()
        merchant_names = {"Dealer", "Private Seller"}
        for merchant_name in merchant_names:
            to_replace = f"This {merchant_name.lower()} is from "
            if to_replace in location:
                return location.replace(to_replace, ""), merchant_name

        return NULL_VALUE, NULL_VALUE

    @property
    def _image_urls(self):
        """Extract the image URLs associated with the listing.

        Returns:
            list: A list of URLs representing images of the listing.
        """
        image_divs = self.html.find_all("div", {"class": "js-carousel-cell"})
        return [
            image_div.find("img")["data-lazy-sweet-spot-master-src"]
            .lower()
            .replace("square_size_", "ExtraLarge")
            for image_div in image_divs
        ]

    @property
    def _badge(self):
        """Get the badge information associated with the listing.

        Returns:
            str: The badge information related to the listing.
        """
        return get_text_html_tag_or_null(
            self.html.find("span", {"class": "article-item-article-badge"})
        )


class DetailedListing:
    """Represents a detailed listing extracted from HTML content."""

    def __init__(self, html):
        """Initialize a DetailedListing object with HTML content.

        Args:
            html (bs4.element.Tag): The HTML content representing the detailed listing.
        """
        self.html = html

    @property
    def json(self):
        """Combine product and logistical details into a JSON representation.

        Returns:
            dict: A dictionary containing the combined information of product and logistical details.
        """
        return {**self._product_details, **self._logistical_details}

    @property
    def _product_details(self):
        """Extract product details from the HTML content.

        Returns:
            dict: A dictionary containing product details extracted from the content.
        """
        product_details = {}
        for tbody in self.html.find_all("tbody"):
            tr_tds = [tr.find_all("td") for tr in tbody.find_all("tr")]
            for idx, tds in enumerate(tr_tds):
                key = get_text_html_tag_or_null(tds[0]).lower().replace(" ", "_")
                # Check if `tds` of length 1 is a header above description column or description body
                if len(tds) == 1:
                    # We want to add description bodies with headers
                    if idx + 1 != len(tr_tds) and len(tr_tds[idx + 1]) == 1:
                        product_details[key] = self._tidy_product_detail(tr_tds[idx + 1][0])
                    continue
                # Add description column key to description
                product_details[key] = self._tidy_product_detail(tds[1])

        return product_details

    @staticmethod
    def _tidy_product_detail(td):
        """Tidy up product detail text.

        Args:
            td (bs4.element.Tag): The HTML tag containing the product detail text.

        Returns:
            str: The cleaned-up product detail text.
        """
        product_detail = get_text_html_tag_or_null(td).replace("\n", " ")
        product_detail = product_detail.replace("Try it on", "").strip()
        return product_detail

    @property
    def _logistical_details(self):
        """Extract logistical details from the HTML content.

        Returns:
            dict: A dictionary containing various logistical details of the listing.
        """
        # Get additional payment / dealer specs
        return {
            "availabe_payments": self._available_payments,
            "anticipated_delivery": self._anticipated_delivery,
            "merchant_name": self._merchant_name,
            "merchant_rating": self._merchant_rating,
            "merchant_reviews": self._merchant_reviews,
            "merchant_badges": self._merchant_badges,
        }

    @property
    def _available_payments(self):
        """Extract available payment methods from the HTML content.

        Returns:
            list: A list of available payment methods for the listing.
        """
        available_payments = []
        payment_keywords = {"visa", "mastercard", "american-express", "bankwire", "affirm"}
        for payment in self.html.find_all("i", {"class": "payment-icon"}):
            payment_class = "".join(payment.get("data-lazy-class", payment.get("class", [])))
            for keyword in payment_keywords:
                if keyword in payment_class:
                    available_payments.append(keyword)
                    break

        return sorted(set(available_payments))

    @property
    def _anticipated_delivery(self):
        """Get the anticipated delivery information from the HTML content.

        Returns:
            str: The anticipated delivery details for the listing.
        """
        anticipated_delivery = self.html.find("span", {"class": "js-shipping-time"})
        return get_text_html_tag_or_null(anticipated_delivery).replace("Anticipated delivery: ", "")

    @property
    def _merchant_name(self):
        """Get the merchant name from the HTML content.

        Returns:
            str: The name of the merchant associated with the listing.
        """
        merchant_name = self.html.find("button", {"class": "js-link-merchant-name"})
        return get_text_html_tag_or_null(merchant_name)

    @property
    def _merchant_rating(self):
        """Get the merchant rating from the HTML content.

        Returns:
            str: The rating of the merchant associated with the listing.
        """
        rating = self.html.find("span", {"class": "rating"})
        return get_text_html_tag_or_null(rating)

    @property
    def _merchant_reviews(self):
        """Get the number of merchant reviews from the HTML content.

        Returns:
            str: The number of reviews for the merchant associated with the listing.
        """
        num_reviews = self.html.find("button", {"class": "js-link-merchant-reviews"})
        return get_text_html_tag_or_null(num_reviews)

    @property
    def _merchant_badges(self):
        """Get the badges associated with the merchant from the HTML content.

        Returns:
            list: A list of badges associated with the merchant of the listing.
        """
        badges = []
        for item in self.html.find_all("button", {"class": "dealer-bonus-badge"}):
            item_html = BeautifulSoup(item.get("data-content"), "html.parser")
            item_badge = item_html.find("span", {"class": ""})
            if item_badge:
                badges.append(get_text_html_tag_or_null(item_badge))

        return badges
