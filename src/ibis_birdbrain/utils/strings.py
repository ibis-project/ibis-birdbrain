# imports


# functions
def estimate_tokens(s: str) -> int:
    """Estimates the number of tokens in a string."""

    return len(s) // 4


def shorten_str(s: str, max_len: int = 27) -> str:
    """Converts a string to a display string."""

    if len(s) > max_len:
        return f"{s[:max_len]}..."
    else:
        return s


def str_to_list_of_str(s: str, max_chunk_len: int = 1000, sep: str = "\n") -> list[str]:
    """Splits a string into a list of strings."""

    result = []

    # TODO: better string chunking algorithm
    # split the string into chunks
    chunks = [s[i : i + max_chunk_len] for i in range(0, len(s), max_chunk_len)]

    # split the chunks into lines
    for chunk in chunks:
        result.extend(chunk.split(sep))

    return result
