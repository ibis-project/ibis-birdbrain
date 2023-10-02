# imports
import requests

from itertools import islice
from html2text import html2text

from ibis_birdbrain.tools import tool


# tools
@tool
def search_internet(
    query: str = "what is the Ibis project?", n_results: int = 8
) -> list[dict[str, str | None]]:
    """Searches the internet for the given query."""
    from duckduckgo_search import DDGS

    ddgs = DDGS()
    return [r for r in islice(ddgs.text(query, backend="lite"), n_results)]


@tool
def webpage_to_str(url: str = "https://ibis-project.org") -> str:
    """Reads a webpage link into a string. Useful for summarizing webpages."""
    response = requests.get(url)
    return html2text(response.text)


@tool
def open_browser(url: str) -> str:
    """Opens the URL in a web browser."""
    try:
        import webbrowser

        webbrowser.open(url.strip("/"))
    except Exception as e:
        return str(e)

    return f"Opened {url} in the user's web browser."
