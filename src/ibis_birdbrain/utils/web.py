# imports
import requests
import webbrowser


from itertools import islice
from html2text import html2text
from duckduckgo_search import DDGS


# functions
def open_browser(url: str) -> str:
    """Opens the URL in a web browser."""
    try:
        webbrowser.open(url.strip("/"))
    except Exception as e:
        return str(e)

    return f"Opened {url} in web browser."


def search_internet(query: str, n_results: int = 10) -> list[dict]:
    """Searches the internet for n results."""
    ddgs = DDGS()
    return [r for r in islice(ddgs.text(query, backend="lite"), n_results)]


def webpage_to_str(url: str = "https://ibis-project.org") -> str:
    """Reads a webpage link into a string."""
    response = requests.get(url)
    return (
        html2text(response.text)
        # .replace("\n", " ")
        # .replace("\r", " ")
        # .replace("\t", " ")
        # .replace("  ", " ")
    )
