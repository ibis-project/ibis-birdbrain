# imports
from marvin import ai_fn


# functions
@ai_fn
def choose_relevant_files(text: str, files: list[str]) -> list[str]:
    """Given input text and a list of files to choose from,
    returns a list of probably relevant files based on their
    path and names."""
    text, files = text, files
    return ""

