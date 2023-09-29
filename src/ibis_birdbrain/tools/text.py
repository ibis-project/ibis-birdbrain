# imports
from ibis_birdbrain.tools import tool

from ibis_birdbrain.models.text import Summary, Translate


# tools
@tool
def summarize_text(text: str) -> Summary:
    """Summarizes text"""
    return Summary(text)


@tool
def translate_text(
    text: str, from_: str = "English (US)", to: str = "Spanish (Mexico)"
) -> Translate:
    """Translates text"""
    text = f"translate `{text}` from {from_} to {to}"
    return Translate(text)
