# imports
import os
import fnmatch

from ibis_birdbrain.tools import tool


# helpers
def read_gitignore(gitignore_path):
    with open(gitignore_path, "r") as f:
        lines = f.readlines()
    return [line.strip() for line in lines if not line.startswith("#")]


def is_ignored(path, ignore_patterns):
    for pattern in ignore_patterns:
        if fnmatch.fnmatch(path, pattern):
            return True
    return False


# tools
@tool
def read_file(path: str) -> str:
    """Reads a file and returns its content."""
    # TODO: fix hack
    if path.startswith("https://") or path.startswith("http://"):
        from ibis_birdbrain.tools.internet import webpage_to_str

        return webpage_to_str(path)
    path = os.path.expanduser(path)
    with open(path, "r") as f:
        return f.read()


@tool
def list_files_and_dirs(
    path: str = ".", depth: int = -1, additional_ignore_dirs: list = []
) -> list[str]:
    """Lists all files and directories in a directory."""
    path = os.path.expanduser(path)
    files_dirs_list = []
    home = os.path.expanduser("~")
    gitignore_path = os.path.join(home, ".gitignore")

    if os.path.exists(gitignore_path):
        gitignore_patterns = read_gitignore(gitignore_path)
    else:
        gitignore_patterns = []

    ignore_dirs = [
        ".git",
        "_site",
        "_output",
        "_freeze",
        ".quarto",
        ".streamlit",
    ] + additional_ignore_dirs

    for root, dirs, files in os.walk(path):
        if root.count(os.sep) >= depth and depth != -1:
            dirs.clear()  # Clear directories list to prevent further depth traversal.

        dirs[:] = [
            d
            for d in dirs
            if not is_ignored(d, ignore_dirs) and not is_ignored(d, gitignore_patterns)
        ]

        for file in files:
            file_path = os.path.join(root, file)
            if not is_ignored(file_path, gitignore_patterns):
                files_dirs_list.append(file_path)

        for d in dirs:
            dir_path = os.path.join(root, d)
            if not is_ignored(dir_path, gitignore_patterns):
                files_dirs_list.append(dir_path)

    return files_dirs_list


@tool
def write_file(path: str, content: str, overwrite: bool = False) -> str:
    """Writes a file."""
    path = os.path.expanduser(path)
    mode = "w" if overwrite else "a"
    with open(path, mode) as f:
        if mode == "a":
            f.write("\n\n")
        f.write(content)

    return f"File written (mode: {mode}) to {path}"
