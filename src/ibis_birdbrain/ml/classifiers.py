# imports
import os
import marvin

from dotenv import load_dotenv

from enum import Enum

from ibis_birdbrain import tasks
from ibis_birdbrain import utils

# config
load_dotenv()
marvin.settings.llm_model = "azure_openai/gpt-4-32k"


# classifiers
def to_ml_classifier(
    options: list[str], docstring: str = "Classifies text based on a list of options"
) -> Enum:
    """Converts a list of options into a ML classifier."""
    enum_dict = {f: f for f in options}
    EnumType = Enum("EnumType", enum_dict)
    EnumType = marvin.ai_classifier(EnumType)
    EnumType.__doc__ = docstring
    return EnumType
