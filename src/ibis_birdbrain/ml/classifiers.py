# imports
import os
import marvin

from dotenv import load_dotenv

from enum import Enum

from ibis_birdbrain import tasks
from ibis_birdbrain import utils

# config
load_dotenv()
marvin.settings.llm_model = "azure_openai/gpt-4"

# classifiers
@marvin.ai_classifier
class Something(Enum):
    something = "Something"
    something_else = "Something else"

# TODO: use Python stuff
#task_types = [(t, t.__doc__) for t in dir(tasks) if not t.startswith("_")]

dirname = os.path.dirname(tasks.__file__)
task_dict = {f: f for f in os.listdir(dirname) if f.endswith(".py") and not f.startswith("_")}
TaskType = Enum("TaskType", task_dict)
TaskType = marvin.ai_classifier(TaskType)

# TODO: use Python stuff
#util_types = [(t, t.__doc__) for t in dir(utils) if not t.startswith("_")]

dirname = os.path.dirname(utils.__file__)
util_dict = {f: f for f in os.listdir(dirname) if f.endswith(".py") and not f.startswith("_")}
UtilType = Enum("UtilType", util_dict)
UtilType = marvin.ai_classifier(UtilType)