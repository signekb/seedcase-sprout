import requests


def get_json_from_url(url: str) -> dict:
    """Gets the JSON object from a URL.

    Args:
        url: A URL with a JSON object to scrape.

    Returns:
        The JSON object from the URL as a dictionary.

    Raises:
        json.JSONDecodeError: If the URL does not contain a JSON object.
        requests.exceptions.ConnectionError: If the URL is not reachable.
        urllib3.exceptions.HTTPError: If the response contains an error status code.
    """
    response = requests.get(url)
    response.raise_for_status()
    return response.json()
