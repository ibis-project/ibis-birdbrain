# imports
from typing import Callable

from ibis_birdbrain.tools import tool
from ibis_birdbrain.tools.code import text_to_python, run_python_code


# tools
@tool
def use_github_cli(text: str = "open the current repo") -> str:
    """Uses the GitHub CLI to fulfill the request via text."""
    text = f"""
    Write a simple Python function to run the `os.system` command using the
    GitHub CLI to fulfill the request via text, e.g.:

    ```python
    import subprocess

    out = subprocess.run(["gh", "repo", "view", "--web"], capture_output=True)
    print(out.stdout.decode())
    ```

    for:

    {text}
    """
    code = text_to_python(text)
    res = run_python_code(code)
    return f"Ran the GitHub CLI successfully! Result: {res}"
