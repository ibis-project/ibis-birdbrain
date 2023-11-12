# imports
from typing import Callable


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
from ibis_birdbrain.tasks.eda import (
    exploratory_data_analysis,
    transform_data,
    visualize_data,
)
from ibis_birdbrain.tasks.code import write_code
from ibis_birdbrain.tasks.learn import learn
from ibis_birdbrain.tasks.information import information
from ibis_birdbrain.tasks.attachments import open_attachments
from ibis_birdbrain.tasks.summarize import (
    summarize_docs,
    summarize_web,
    summarize_databases,
    summarize_tables,
)


tasks = {
    "exploratory_data_analysis": exploratory_data_analysis,
    "transform_data": transform_data,
    "write_code": write_code,
    "visualize_data": visualize_data,
    "learn": learn,
    "information": information,
    "open_attachments": open_attachments,
    "summarize_docs": summarize_docs,
    "summarize_web": summarize_web,
    "summarize_databases": summarize_databases,
    "summarize_tables": summarize_tables,
}
tasks = Tasks(tasks)

__all__ = ["tasks"]
