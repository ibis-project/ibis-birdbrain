# imports
import marvin

from dotenv import load_dotenv

from enum import Enum

# config
load_dotenv()
marvin.settings.llm_model = "azure_openai/gpt-4-32k"


# classifiers
def to_ml_classifier(
    options: list[str], instructions: str = "Classifies text based on a list of options"
) -> Enum:
    """Converts a list of options into a ML classifier."""
    enum_dict = {f: f for f in options}
    EnumType = Enum("EnumType", enum_dict)
    EnumType = marvin.ai_classifier(EnumType)
    EnumType.__doc__ = instructions
    return EnumType
