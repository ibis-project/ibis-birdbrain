# imports
from ibis_birdbrain.tasks import Task

from ibis_birdbrain.messages import Messages, Message, Email


# classes
class PythonCode(Task):
    """
    Python code.
    """

    def __init__(self, name: str = "write_python_code"):
        super().__init__(name=name)

    def __call__(self, m: Message) -> Message:
        """Run the Python code."""
        m = Email(body="Python code running.")
        return m
