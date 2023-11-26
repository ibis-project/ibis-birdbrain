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
    """Generates a response to messages."""


@marvin.ai_fn
def filter_messages(
    ms: str,
    instructions: str = "",
) -> list[str]:
    """Filters messages."""


@marvin.ai_fn
def filter_subsystems(
    ms: str,
    instructions: str = "",
) -> list[str]:
    """Filters subsystems."""


@marvin.ai_fn
def filter_attachments(
    ms: str,
    instructions: str = "",
) -> list[str]:
    """Filters attachments."""
