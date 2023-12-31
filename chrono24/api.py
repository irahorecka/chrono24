import re
from functools import lru_cache

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://chrono24.com"
NULL_VALUE = "null"


def get_attr_text_or_null(attr):
    attr_text = attr.text.strip() if attr else ""
    return attr_text or NULL_VALUE


class chrono24:
    base_query_url = BASE_URL + "/search/index.htm?dosearch=true&query="
    page_size = 120

    def __init__(self, query):
        self.query = query

    def search(self, limit=None):
        yield from self._search(self._get_standard_listing, limit)

    def search_detail(self, limit=None):
        yield from self._search(self._get_detailed_listing, limit)

    def _search(self, get_listing, limit):
        # Get HTML content for the first page to find total page count for query
        # `sortorder=5` sorts for newest listings
        listings = self._get_listings(pageSize=self.page_size, showPage=1, sortorder=5)
        total_page_count = self._get_total_page_count(listings)
        if not total_page_count:
            return
        # Iterate through all pages and yield individual listings as JSON
        num_listings_yielded = 0
        for page_number in range(1, total_page_count + 1):
            # First page of query URL already declared - simply yield its listings
            if page_number != 1:
                listings = self._get_listings(
                    pageSize=self.page_size, showPage=page_number, sortorder=5
                )
            for listing in listings:
                if limit and num_listings_yielded >= limit:
                    return
                yield get_listing(listing)
                num_listings_yielded += 1

    def _get_total_page_count(self, listings):
        try:
            return listings.total_listing_count // self.page_size + 1
        # Unable to get total listing count because of invalid query
        except AttributeError:
            print(f"'{self.query}' is not a valid query.")
            return None

    def _get_listings(self, **kwargs):
        query_url = self.base_query_url + self.query.replace(" ", "+")
        modified_query_url = Session.get_response(query_url).url + self._join_attrs(**kwargs)
        page_number = kwargs.get("showPage", 1)
        if page_number != 1:
            modified_query_url = modified_query_url.replace("index.htm", f"index-{page_number}.htm")

        return Listings(Session.get_html(modified_query_url))

    def _get_standard_listing(self, listing):
        return listing.json

    def _get_detailed_listing(self, listing):
        return {**listing.json, **DetailedListing(Session.get_html(listing.json["url"])).json}

    @staticmethod
    def _join_attrs(**kwargs):
        return "&" + "&".join(f"{k}={v}" for k, v in kwargs.items())


class Listings:
    def __init__(self, html):
        self.html = html

    def __iter__(self):
        listings_div = self.html.find("div", {"id": "wt-watches"})
        if not listings_div:
            print("No listing found.")
            return None
        listings = listings_div.find_all("a", {"class": "js-article-item"})
        for listing in listings:
            yield StandardListing(listing)

    @property
    def total_listing_count(self):
        re_pattern_comma_sep_num = r"\b\d{1,3}(?:,\d{3})*\b"
        listing_count_text = get_attr_text_or_null(
            self.html.find("div", {"class": "h1 m-b-0 m-t-0"})
        )
        match = re.search(re_pattern_comma_sep_num, listing_count_text)
        # Return total listing count as integer, otherwise 0
        return int(match.group().replace(",", "")) if match else 0


class StandardListing:
    def __init__(self, html):
        self.html = html

    @property
    @lru_cache(maxsize=128)
    def json(self):
        return {
            **{
                "id": self.html["data-article-id"].strip(),
                "url": BASE_URL + self.html["href"].strip(),
                "manufacturer": self.html["data-manufacturer"].strip(),
                "certification_status": self.html["data-watch-certification-status"].strip(),
                "title": get_attr_text_or_null(
                    self.html.find("div", {"class": "text-bold text-ellipsis"})
                ),
                "description": get_attr_text_or_null(
                    self.html.find("div", {"class": "text-ellipsis m-b-2"})
                ),
                "price": get_attr_text_or_null(
                    (lambda x: x.parent if x else x)(self.html.find("span", {"class": "currency"}))
                ),
            },
            **self._shipping_price,
            **self._location_and_seller,
            **self._badge,
            **self._image_urls,
        }

    @property
    def _shipping_price(self):
        shipping_price_text = get_attr_text_or_null(
            self.html.find("div", {"class": "text-muted text-sm"})
        )
        re_pattern_shipping_cost = r"\b\d{1,3}(?:,\d{3})*\b"
        match = re.search(re_pattern_shipping_cost, shipping_price_text)
        return {"shipping_price": f'${match.group() if match else "0"}'}

    @property
    def _location_and_seller(self):
        location = self.html.find("button", {"class": "js-tooltip"})["data-content"].strip()[:-1]
        sellers = ("dealer", "private seller")
        for seller in sellers:
            to_replace = f"This {seller} is from "
            if to_replace in location:
                return {"location": location.replace(to_replace, ""), "seller": seller}

        return {"location": NULL_VALUE, "seller": NULL_VALUE}

    @property
    def _image_urls(self):
        image_divs = self.html.find_all("div", {"class": "js-carousel-cell"})
        return {
            "image_urls": [
                image_div.find("img")["data-lazy-sweet-spot-master-src"]
                .lower()
                .replace("square_size_", "ExtraLarge")
                for image_div in image_divs
            ]
        }

    @property
    def _badge(self):
        return {
            "badge": get_attr_text_or_null(
                self.html.find("span", {"class": "article-item-article-badge"})
            )
        }


class DetailedListing:
    def __init__(self, html):
        self.html = html

    @property
    def json(self):
        return {**self._product_details, **self._logistical_details}

    @property
    def _product_details(self):
        product_details = {}
        for tbody in self.html.find_all("tbody"):
            for tr in tbody.find_all("tr"):
                tds = tr.find_all("td")
                if len(tds) < 2:
                    continue
                product_details[
                    get_attr_text_or_null(tds[0]).lower().replace(" ", "_")
                ] = self._tidy_product_detail(tds[1])

        return product_details

    @staticmethod
    def _tidy_product_detail(td):
        product_detail = get_attr_text_or_null(td).replace("\n", " ")
        product_detail = product_detail.replace("Try it on", "").strip()
        return product_detail

    @property
    def _logistical_details(self):
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
        anticipated_delivery = self.html.find("span", {"class": "js-shipping-time"})
        return get_attr_text_or_null(anticipated_delivery).replace("Anticipated delivery: ", "")

    @property
    def _merchant_name(self):
        merchant_name = self.html.find("button", {"class": "js-link-merchant-name"})
        return get_attr_text_or_null(merchant_name)

    @property
    def _merchant_rating(self):
        rating = self.html.find("span", {"class": "rating"})
        return get_attr_text_or_null(rating)

    @property
    def _merchant_reviews(self):
        num_reviews = self.html.find("button", {"class": "js-link-merchant-reviews"})
        return get_attr_text_or_null(num_reviews)

    @property
    def _merchant_badges(self):
        badges = []
        for item in self.html.find_all("button", {"class": "dealer-bonus-badge"}):
            item_html = BeautifulSoup(item.get("data-content"))
            item_badge = item_html.find("span", {"class": ""})
            if item_badge:
                badges.append(get_attr_text_or_null(item_badge))

        return badges


class Session:
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate",
        "accept-language": "pt-PT,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        "cookie": "uid=9c718efe-dcca-4e71-b92d-c3dd7b7f06cc",
        "referer": "https://a3853408329f84107a5d2b90c11d7c4b.safeframe.googlesyndication.com/",
        "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36",
    }

    @classmethod
    def get_html(cls, url):
        return BeautifulSoup(cls.get_response(url).text, parser="html.parser")

    @classmethod
    def get_response(cls, url):
        return requests.get(url, headers=cls.headers)
