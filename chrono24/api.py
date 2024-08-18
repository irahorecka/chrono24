"""
chrono24/api
~~~~~~~~~~~~
"""

import json
import re
import time
from functools import lru_cache

from bs4 import BeautifulSoup

from chrono24.exceptions import NoListingsFoundException
from chrono24.session import get_html, get_response

BASE_URL = "https://chrono24.com"
NULL_VALUE = "null"
RE_PATTERN_COMMA_SEPARATED_NUM = r"\b\d{1,3}(?:,\d{3})*\b"


def get_html_tag_as_text(html_tag):
    """Get the text from an HTML tag or return NULL_VALUE if the tag is None or has no text.

    Args:
        html_tag (bs4.element.Tag or None): The HTML tag to extract text from.

    Returns:
        str: The text content of the HTML tag, or NULL_VALUE if the tag is None or has no text.
    """
    html_tag_text = html_tag.text.strip() if html_tag else ""
    return html_tag_text or NULL_VALUE


def get_html_tag_attribute_as_text(html_tag, attr):
    """Get the attribute text from an HTML tag or return NULL_VALUE if the tag is None or has no text.

    Args:
        html_tag (bs4.element.Tag or None): The HTML tag to extract text from.
        attr (str): Attribute to find in the HTML tag.

    Returns:
        str: The attribute text content of the HTML tag, or NULL_VALUE if the tag is None or has no text.
    """
    # Get attribute text from HTML tag or return NULL_VALUE if tag is None
    html_tag_text = html_tag.get(attr, "").strip() if html_tag else ""
    return html_tag_text or NULL_VALUE


class Chrono24:
    """A class for performing searches on Chrono24."""

    page_size = 120

    def __init__(self, query):
        """Initialize a chrono24 object with a query.

        Args:
            query (str): The search query to be performed.
        """
        self.url = get_response(
            f"{BASE_URL}/search/index.htm?dosearch=true&query={query.replace(' ', '+')}"
        ).url
        self.count = self._get_listings().count

    def search(self, limit=None):
        """Perform a search using the _search method with an optional limit.

        Args:
            limit (int, optional): An optional integer representing the maximum number of results to return.

        Yields:
            Iterator[dict]: Listings as JSON found from search.
        """
        yield from self._search(self._get_standard_listing_as_json, limit)

    def search_detail(self, limit=None):
        """Perform a detailed search using the _search method with an optional limit.

        Args:
            limit (int, optional): An optional integer representing the maximum number of detailed results to return.

        Yields:
            Iterator[dict]: Detailed listings as JSON found from search.
        """
        yield from self._search(self._get_detailed_listing_as_json, limit)

    def _search(self, get_listing_as_json, limit):
        """Perform a search and yield individual listings based on the given get_listing_as_json function.

        Args:
            get_listing_as_json (function): A function to process individual listings as JSON.
            limit (int, optional): The maximum number of listings to yield. Defaults to None.

        Yields:
            dict: A processed listing JSON obtained from the search results.
        """
        # Get HTML content for the first listings page to find total page count for a query
        request_attrs = {
            "pageSize": self.page_size,  # Number of listings per results page
            "showPage": 1,  # What page to view
            "sortorder": 5,  # Sort by newest listings
        }
        # Construct Listings instance
        listings = self._get_listings(**request_attrs)
        # Iterate through all listings pages and yield individual listings
        num_listings_yielded = 0
        for page_number in range(1, self._total_page_count + 1):
            # First page of listings URL is already declared - simply yield its listings
            if page_number != 1:
                request_attrs["showPage"] = page_number
                listings = self._get_listings(**request_attrs)
            for listing_html in listings.htmls:
                # Check if user-specified limit is reached
                if limit and num_listings_yielded >= limit:
                    return
                yield get_listing_as_json(listing_html)
                num_listings_yielded += 1

    def _get_listings(self, **kwargs):
        """Get Listings instance based on the provided URL attribute keyword arguments.

        Args:
            **kwargs: URL attributes for customizing the query URL.

        Returns:
            Listings: A Listings object containing the fetched listings.
        """
        # Chrono24 will modify the initial query URL - add URL attributes to the modified URL
        listings_url = self.url + self._join_attrs(**kwargs)
        page_number = kwargs.get("showPage", 1)
        # Further modify URL if seeking a listings page greater than 1
        if page_number != 1:
            listings_url = listings_url.replace(".htm", f"-{page_number}.htm")

        return self._get_listings_with_attempts(listings_url, max_attempts=8)

    @property
    def _total_page_count(self):
        """Calculate the total number of pages based on the total listing count.

        Returns:
            int: The total number of pages calculated based on the total listing count.
        """
        return self.count // self.page_size + 1

    @staticmethod
    def _get_standard_listing_as_json(listing_html):
        """Get the standard JSON representation of a listing.

        Args:
            listing_html (bs4.element.Tag): The HTML content representing the listing.

        Returns:
            dict: The standard JSON representation of the listing.
        """
        return StandardListing(listing_html).json

    @staticmethod
    def _get_detailed_listing_as_json(listing_html):
        """Get a detailed JSON representation of a listing by combining its standard JSON
        with additional details fetched from its URL.

        Args:
            listing_html (bs4.element.Tag): The HTML content representing the listing.

        Returns:
            dict: The detailed JSON representation of the listing.
        """
        listing = StandardListing(listing_html)
        listing_url = listing.json["url"]
        detailed_listing = DetailedListing(get_html(listing_url))
        return {**listing.json, **detailed_listing.json}

    @staticmethod
    def _join_attrs(**kwargs):
        """Join keyword arguments into a URL query string format.

        Args:
            **kwargs: URL attibutes to be joined into a query string.

        Returns:
            str: A string representation of the joined URL query parameters.
        """
        return "&" + "&".join(f"{k}={v}" for k, v in kwargs.items())

    @staticmethod
    def _get_listings_with_attempts(listings_url, max_attempts=5):
        """Get Listings instance with a maximum number of attempts.

        Args:
            listings_url (str): The URL to fetch listings from.
            max_attempts (int, optional): The maximum number of attempts to fetch listings. Defaults to 5.

        Returns:
            Listings: A Listings object containing the fetched listings.
        """
        attempts = 0
        while attempts < max_attempts:
            try:
                listings = Listings(get_html(listings_url))
                # Return Listings instance if no AttributeError is raised
                next(listings.htmls)  # Check if listings are found
                return listings
            except AttributeError:
                attempts += 1
                print(f"Retrying HTML parsing... Attempt # {attempts}.")
                time.sleep(1)  # Wait 1 second before retrying


class Listings:
    """A class representing a collection of listings extracted from HTML content."""

    def __init__(self, html):
        """Initialize the Listings object with HTML content.

        Args:
            html (bs4.element.ResultSet): The HTML content containing listings.
        """
        self.html = html
        self.count = self._get_total_count(html)

    @property
    def htmls(self):
        """Iterate through the listings and yield individual listing HTML content.

        Yields:
            bs4.element.Tag: The HTML content representing the listing.
        """
        listings_div = self.html.find("div", {"id": "wt-watches"})
        # Yield individual listings as found in listings page
        yield from listings_div.find_all("a", {"class": re.compile(r"^js-article-item")})

    @staticmethod
    def _get_total_count(html):
        """Get the total count of listings from the HTML content.

        Args:
            html (bs4.element.ResultSet): The HTML content containing listings.

        Returns:
            int: The total count of listings as an integer.

        Raises:
            NoListingsFoundException: Raised if the query is invalid or no listing count is found.
        """
        # Find the script tag that contains `window.metaData`
        script = html.find("script", string=re.compile("window.metaData"))
        # Use regex to extract the JSON string
        pattern = re.compile(r"window.metaData = ({.*?});", re.DOTALL)
        script_text = script.text
        match = pattern.search(script_text)
        if match:
            metadata_json_str = match[1]
            metadata = json.loads(metadata_json_str)
            # Only return total count if listings are found
            total_count = int(metadata["data"]["searchResult"]["numResult"])
            if total_count > 0:
                return total_count

        raise NoListingsFoundException("No listings found.")


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
            "id": get_html_tag_attribute_as_text(self.html, "data-article-id"),
            "url": BASE_URL + get_html_tag_attribute_as_text(self.html, "href"),
            "manufacturer": get_html_tag_attribute_as_text(self.html, "data-manufacturer"),
            "certification_status": get_html_tag_attribute_as_text(
                self.html, "data-watch-certification-status"
            ),
            "title": get_html_tag_as_text(
                self.html.find(
                    "div", class_=lambda x: x and "text-bold" in x and "text-ellipsis" in x
                )
            ),
            "description": get_html_tag_as_text(
                self.html.find("div", class_=lambda x: x and "m-b-2" in x and "text-ellipsis" in x)
            ),
            "price": get_html_tag_as_text(
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
        # Extract comma-separated shipping price
        shipping_price_text = get_html_tag_as_text(
            self.html.find("div", {"class": "text-muted text-sm"})
        )
        match = re.search(RE_PATTERN_COMMA_SEPARATED_NUM, shipping_price_text)
        return f'${match.group() if match else "0"}'

    @property
    @lru_cache(maxsize=64)
    def _location_and_merchant_name(self):
        """Get the location and merchant name from the HTML content.

        Returns:
            tuple: A tuple containing the location and merchant name extracted from the content.
        """
        location = get_html_tag_attribute_as_text(
            self.html.find("button", {"class": "js-tooltip"}), "data-content"
        )
        # Possible merchant names found in listings page
        merchant_names = {"Dealer", "Private Seller"}
        for merchant_name in merchant_names:
            # Return simplified location and seller if a location is successfully simplified
            to_replace = f"This {merchant_name.lower()} is from "
            if to_replace in location:
                return location.replace(to_replace, ""), merchant_name

        # No merchant was found - return full location and null value
        return location, NULL_VALUE

    @property
    def _image_urls(self):
        """Extract the image URLs associated with the listing.

        Returns:
            list: A list of URLs representing images of the listing.
        """
        image_divs = self.html.find_all("div", {"class": "js-carousel-cell"})
        # Modify URLs to select for extra large images
        return [
            get_html_tag_attribute_as_text(image_div.find("img"), "data-lazy-sweet-spot-master-src")
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
        badge = self.html.find("span", {"class": "article-item-article-badge"})
        return get_html_tag_as_text(badge)


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
        for detail_section in self.html.find_all("tbody"):
            # Each table row is either a detail column (key-value pair) or a detail header or body
            details = [section.find_all("td") for section in detail_section.find_all("tr")]
            for idx, detail in enumerate(details):
                # Get detail key and set default detail value
                detail_key = get_html_tag_as_text(detail[0]).lower().replace(" ", "_")
                detail_description = NULL_VALUE
                try:
                    detail_description = get_html_tag_as_text(detail[1])
                    product_details[detail_key] = self._tidy_product_detail(detail_description)
                except IndexError:
                    # Check if `detail` is a header above description column or description body
                    # We want to map description headers to their bodies
                    if idx + 1 != len(details) and len(details[idx + 1]) == 1:
                        detail_description = get_html_tag_as_text(details[idx + 1][0])
                        product_details[detail_key] = self._tidy_product_detail(detail_description)

        return product_details

    @staticmethod
    def _tidy_product_detail(product_detail):
        """Tidy up product detail text.

        Args:
            product_detail (str): The product detail text.

        Returns:
            str: The cleaned-up product detail text.
        """
        # Add statements as necessary to tidy possible product detail values
        product_detail = product_detail.replace("\n", " ")
        # Simplify case diameter value
        product_detail = product_detail.replace("Try it on", "").strip()
        return product_detail

    @property
    def _logistical_details(self):
        """Extract logistical details from the HTML content.

        Returns:
            dict: A dictionary containing various logistical details of the listing.
        """
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
        payment_keywords = {"visa", "mastercard", "american-express", "bankwire", "affirm"}
        available_payments = []
        for payment in self.html.find_all("i", {"class": "payment-icon"}):
            # Available payments will be found in the payment attributes class
            payment_class = "".join(payment.get("data-lazy-class", payment.get("class", [])))
            for keyword in payment_keywords:
                if keyword in payment_class:
                    available_payments.append(keyword)
                    break

        # Duplicate payment keywords may exist - only keep unique keywords
        return sorted(set(available_payments))

    @property
    def _anticipated_delivery(self):
        """Get the anticipated delivery information from the HTML content.

        Returns:
            str: The anticipated delivery details for the listing.
        """
        anticipated_delivery = self.html.find("span", {"class": "js-shipping-time"})
        return get_html_tag_as_text(anticipated_delivery).replace("Anticipated delivery: ", "")

    @property
    def _merchant_name(self):
        """Get the merchant name from the HTML content.

        Returns:
            str: The name of the merchant associated with the listing.
        """
        merchant_name = self.html.find("button", {"class": "js-link-merchant-name"})
        return get_html_tag_as_text(merchant_name)

    @property
    def _merchant_rating(self):
        """Get the merchant rating from the HTML content.

        Returns:
            str: The rating of the merchant associated with the listing.
        """
        rating = self.html.find("span", {"class": "rating"})
        return get_html_tag_as_text(rating)

    @property
    def _merchant_reviews(self):
        """Get the number of merchant reviews from the HTML content.

        Returns:
            str: The number of reviews for the merchant associated with the listing.
        """
        num_reviews = self.html.find("button", {"class": "js-link-merchant-reviews"})
        return get_html_tag_as_text(num_reviews)

    @property
    def _merchant_badges(self):
        """Get the badges associated with the merchant from the HTML content.

        Returns:
            list: A list of badges associated with the merchant of the listing.
        """
        badges = []
        for badge in self.html.find_all("button", {"class": "dealer-bonus-badge"}):
            badge_html = BeautifulSoup(badge.get("data-content"), "html.parser")
            badge_text = badge_html.find("span", {"class": ""})
            if badge_text:
                badges.append(get_html_tag_as_text(badge_text))

        return badges
