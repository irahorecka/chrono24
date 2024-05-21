"""
chrono24/session
~~~~~~~~~~~~~~~~
"""

import requests
import tenacity
from bs4 import BeautifulSoup

from chrono24.exceptions import RequestException

HEADERS = {
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
    "user-agent": "Mozilla/5.0 (Windows NT 8.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36",
}


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
                *args, **kwargs, headers={**HEADERS, **kwargs.get("headers", {})}
            )
            response.raise_for_status()
            return response
