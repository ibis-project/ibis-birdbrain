"""
ML functions for Ibis Birdbrain use Marvin AI functions
as general-purpose functions for LLM-powered functionality.
"""

# imports
import marvin

from dotenv import load_dotenv

# config
load_dotenv()
marvin.settings.llm_model = "azure_openai/gpt-4-32k"


# functions
@marvin.ai_fn
def write_response(
    ms: str,
    instructions: str = "",
) -> str:
    """Generates a response (message body only) to messages."""


@marvin.ai_fn
def filter_messages(
    ms: str,
    instructions: str = "",
) -> list[str]:
    """Filters messages based on the context
    from the messages and instructions."""


@marvin.ai_fn
def filter_attachments(
    ms: str,
    options: list[str],
    instructions: str = "",
) -> list[str]:
    """Filters attachments from the options,
    returning a list of GUIDs based on the context
    from the messages and instructions."""


@marvin.ai_fn
def filter_tables(
    ms: str,
    options: list[str],
    instructions: str = "",
) -> list[str]:
    """Filters tables from the options,
    returning a list of table names based on the context
    from the messages and instructions."""
