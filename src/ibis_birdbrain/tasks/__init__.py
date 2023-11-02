# imports
from typing import Callable
from ibis_birdbrain.tasks.eda import summarize_databases, summarize_table


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


# exports
tasks = {
    "summarize_databases": summarize_databases,
    "summarize_table": summarize_table,
}
tasks = Tasks(tasks)

__all__ = ["tasks"]
