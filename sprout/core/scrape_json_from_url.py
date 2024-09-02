from requests import get


def scrape_json_from_url(url: str) -> dict:
    """Scrapes a URL with a JSON object.

    Args:
        url: URL with JSON object to scrape.

    Returns:
        A dictionary with the JSON object from the URL.

    Raises:
        json.JSONDecodeError: If the URL does not contain a JSON object.
        requests.exceptions.ConnectionError: If the URL is not reachable.
    """
    return get(url).json()
