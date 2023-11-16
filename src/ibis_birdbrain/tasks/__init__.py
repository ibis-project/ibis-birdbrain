"""
Tasks in Ibis Birdbrain are tasks the bot can perform on behalf of the user.

All tasks are message -> message functions.

High-level tasks additionally return a list of system messages.
This is sorta a hack.
"""

# imports
from typing import Callable

from ibis_birdbrain.messages import Messages
from ibis_birdbrain.ml.classifiers import to_ml_classifier


# classes
class Tasks:
    tasks: dict[str, Callable]

    def __init__(self, tasks):
        self.tasks = tasks

    def __str__(self):
        s = ""
        for task_name, task_func in self.tasks.items():
            s += f"**name**: {task_name}\n**description**: {task_func.__doc__}\n---\n"

        return s

    def __repr__(self):
        return str(self)

    def __getitem__(self, key):
        return self.tasks[key]

    def __setitem__(self, key, value):
        self.tasks[key] = value

    def __delitem__(self, key):
        del self.tasks[key]

    def select(self, m: Messages, text: str):
        """Get a task from the messages."""
        selection_options = list(self.tasks.keys())
        selection_classifier = to_ml_classifier(
            selection_options,
            instructions=f"Choose a task from {self} with context {m} based on the request of {text}",
        )
        selection = selection_classifier(text).value
        return self.tasks[selection]


# exports
from ibis_birdbrain.tasks.eda import eda
from ibis_birdbrain.tasks.code import code
from ibis_birdbrain.tasks.learn import learn
from ibis_birdbrain.tasks.summarize import summarize

tasks = {
    eda.__doc__: eda,
    code.__doc__: code,
    learn.__doc__: learn,
    summarize.__doc__: summarize,
}
tasks = Tasks(tasks)

__all__ = ["Tasks", "tasks"]
