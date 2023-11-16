"""
ML functions for Ibis Birdbrain use Marvin AI functions
as general-purpose functions for LLM-powered functionality.
"""

# imports
import marvin

from dotenv import load_dotenv

from ibis.expr.schema import Schema

from ibis_birdbrain.messages import Messages
from ibis_birdbrain.attachments import DataAttachment, TableAttachment


# config
load_dotenv()
marvin.settings.llm_model = "azure_openai/gpt-4-32k"


# functions
@marvin.ai_fn
def generate_response(
    m: Messages,
    instructions: str = "",
    additional_instructions: str = "",
    additional_context: str = "",
) -> str:
    """Generates a response from an email."""


@marvin.ai_fn
def filter_attachments(
    m: Messages,
    task_type: str = "eda",
) -> list[str]:
    """Filters relevant attachments from messages, returning a list of GUIDs of only relevant attachments per the text."""
