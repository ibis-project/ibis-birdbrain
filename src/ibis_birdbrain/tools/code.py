# imports
from ibis_birdbrain.tools import tool

from io import StringIO
from contextlib import redirect_stdout, redirect_stderr

from ibis_birdbrain.functions.code import (
    gen_python_code,
    fix_python_code,
)


# tools
@tool
def text_to_python(question: str) -> str:
    """Returns a Python code given text."""
    return gen_python_code(question)


@tool
def fix_python_error(code: str, error: str) -> str:
    """Fixes a Python error in the code."""
    return fix_python_code(code, error)


@tool
def python_function_to_udf(code: str) -> str:
    """Converts a Python function to an Ibis UDF."""
    return f"""
import ibis

@ibis.udf.scalar.python
{code}""".strip()


@tool
def run_python_code(code: str) -> str:
    """Execute Python code as a string and return the output"""
    code = f"""
import subprocess

def run_code():
    {code}

out = subprocess.run(run_code(), capture_output=True, text=True)

return out.stdout, out.stderr"""

    try:
        local_vars = {}
        exec(code, globals(), local_vars)
        stdout, stderr = local_vars["out"]
    except Exception as e:
        stdout = ""
        stderr = f"Error: {e}"

    return f"Code ran successfully!\nstdout: {stdout}\nstderr: {stderr}"
