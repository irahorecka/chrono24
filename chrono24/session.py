"""
chrono24/session
~~~~~~~~~~~~~~~~
"""

import requests
import tenacity
from bs4 import BeautifulSoup
from faker import Faker

from chrono24.exceptions import RequestException


def _log_retry_attempt(retry_state):
    """Logs retry state to console if request retry failed.

    Args:
        retry_state (tenacity.retry): Retry object.
    """
    print(f"Retrying request... Attempt #{retry_state.attempt_number}.")


RETRY_ARGS = {
    "wait": tenacity.wait.wait_random_exponential(multiplier=1, exp_base=2),
    "retry": tenacity.retry_if_exception_type(
        (
            requests.ConnectionError,
            requests.HTTPError,
            requests.RequestException,
        )
    ),
    "before_sleep": _log_retry_attempt,
}


def get_html(url, error_message="Failed to execute request.", max_attempts=8):
    """Takes URL and converts to `bs4.BeautifulSoup` object. Retries requests for `max_attempts` if request fails;
    if request still fails thereafter, None is returned.

    Args:
        url (str): URL to query and convert to `bs4.BeautifulSoup` object.
        error_message (str, optional): Error message to print if requests failed. Defaults to "Failed to
            execute request."
        max_attempts (int, optional): Maximum number of re-attempts prior to forfeiting request. Defaults
            to 8.

    Returns:
        bs4.BeautifulSoup: `bs4.BeautifulSoup` object if requested response was successful.

    Raises:
        RequestException: Repeated requests failed altogether.
    """
    response = get_response(url, error_message=error_message, max_attempts=max_attempts)
    return BeautifulSoup(response.text, "html.parser")


def get_response(*args, error_message="Failed to execute request.", max_attempts=8, **kwargs):
    """Makes get request using the tenacity wrapper to retry failed requests. Returns response object if
    request is successful; returns None if request failed after max retries.

    Args:
        *args (Any): Positional arguments to pass to `requests.Session().get`.
        error_message (str, optional): Error message to print if requests failed. Defaults to "Failed to
            execute request."
        max_attempts (int, optional): Maximum number of re-attempts prior to forfeiting request. Defaults
            to 8.
        **kwargs (Any): Keyword arguments to pass to `requests.Session().get`.

    Returns:
        requests.models.Response: Returns response if request was successful.

    Raises:
        RequestException: Repeated requests failed altogether.
    """
    try:
        return _get_tenacity_wrapped_response(*args, max_attempts=max_attempts, **kwargs)
    except (tenacity.RetryError, requests.exceptions.HTTPError) as e:
        print(error_message)
        raise RequestException from e


def _get_tenacity_wrapped_response(*args, max_attempts=8, **kwargs):
    """Makes tenacity-wrapped get request and retries request if it fails.

    Args:
        *args (Any): Positional arguments to pass to `requests.Session().get`.
        max_attempts (int): Maximum number of re-attempts prior to forfeiting request. Defaults to 8.
        **kwargs (Any): Keyword arguments to pass to `requests.Session().get`.

    Returns:
        requests.models.Response : Returns response and session object if request was successful.

    Raises:
        tenacity.RetryError: Failed to get request after max retries.
        requests.exceptions.HTTPError: An HTTP error occurred.
    """
    retry_args = RETRY_ARGS.copy()
    retry_args["stop"] = tenacity.stop.stop_after_attempt(max_attempts)
    for attempt in tenacity.Retrying(**retry_args):
        with attempt:
            response = requests.get(
                *args,
                **kwargs,
                headers={**_generate_dom_specific_header(), **kwargs.get("headers", {})},
            )
            response.raise_for_status()
            return response


def _generate_dom_specific_header():
    """Generates high-quality DOM-specific HTTP header using the Faker library, ensuring maximum authenticity
    and variability to mimic real browser behavior.

    Returns:
        dict: A dictionary containing dynamically generated HTTP headers.
    """
    # Initialize Faker instance
    faker = Faker()
    # Generate a realistic User-Agent and associated fields using the available methods
    user_agent = faker.user_agent()
    # Use available platform tokens and operating system attributes from Faker
    platform_token = faker.random_element(
        elements=[
            faker.windows_platform_token(),
            faker.linux_platform_token(),
            faker.mac_platform_token(),
        ]
    )
    # Generate the headers using only the Faker methods listed in the provided attribute list
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",  # Commonly supported encoding formats in browsers
        "Accept-Language": faker.language_code(),  # Use language_code to generate values like 'en', 'de', etc.
        "Cache-Control": "no-cache, no-store, must-revalidate",  # Ensure no caching for the request
        "Connection": "keep-alive",  # Standard for persistent connections
        "DNT": "1" if faker.boolean() else "0",  # Do Not Track: 1 or 0
        "Host": faker.domain_name(),  # Simulate a real host domain
        "Origin": faker.uri(),  # Generate an origin header using a realistic URI
        "Pragma": "no-cache",  # Prevent any caching
        "Referer": faker.url(),  # Generates a referer URL to simulate legitimate navigation
        "Sec-CH-UA": f'"{user_agent}";v="{faker.random_int(80, 116)}", "{platform_token}";v="{faker.random_int(80, 116)}"',
        "Sec-CH-UA-Mobile": "?0",  # Indicates a desktop environment
        "Sec-CH-UA-Platform": f'"{platform_token}"',  # Randomized platform token from Faker
        "Sec-Fetch-Dest": "document",  # Specifies that the resource is a document
        "Sec-Fetch-Mode": "navigate",  # Request made by navigating
        "Sec-Fetch-Site": "same-origin",  # Indicates request is from the same origin
        "Sec-Fetch-User": "?1",  # User-initiated navigation
        "TE": "Trailers",  # HTTP Transfer-Encoding
        "Upgrade-Insecure-Requests": "1",  # Requests secure (HTTPS) versions
        "User-Agent": user_agent,  # Use the same user-agent string as generated earlier
        "X-Forwarded-For": faker.ipv4_public(),  # Generate a realistic public IP address
        "Authorization": f"Bearer {faker.uuid4()}",  # Simulate a Bearer token using a UUID
    }
    return headers
