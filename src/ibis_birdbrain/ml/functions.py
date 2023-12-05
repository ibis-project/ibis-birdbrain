"""
ML functions for Ibis Birdbrain use Marvin AI functions
as general-purpose functions for LLM-powered functionality.
"""

# imports
import os
import marvin

from dotenv import load_dotenv

# config
load_dotenv()
marvin.settings.llm_model = "azure_openai/gpt-4-32k"


@marvin.ai_fn
def test(
    about: str = "pair programming with AI",
    haiku: bool = False,
) -> str:
    """Test function. Respond with a random poem."""


# functions
@marvin.ai_fn
def write_response(
    messages: list[str],
    instructions: str = "",
) -> str:
    """Generates a response (message body ONLY -- DO NOT write message metadata) to messages."""


@marvin.ai_fn
def filter_messages(
    messages: list[str],
    instructions: str = "",
) -> list[str]:
    """Filters messages based on the context
    from the messages and instructions."""


@marvin.ai_fn
def filter_attachments(
    messages: list[str],
    options: list[str],
    instructions: str = "",
) -> list[str]:
    """Filters attachments from the options,
    returning a list of GUIDs based on the context
    from the messages and instructions."""


@marvin.ai_fn
def filter_tables(
    message: str,
    options: list[str],
    instructions: str = "",
) -> list[str]:
    """Filters tables from the options,
    returning a list of table names based on the context
    from the messages and instructions."""


@marvin.ai_fn
def write_task_message(
    messages: list[str],
    instructions: str = "",
) -> str:
    """Generates a task message (message body only) to messages."""


@marvin.ai_fn
def write_sql_query(
    ms: str,
    table_names: list[str],
    table_schemas: list[str],
    instructions: str = "",
) -> str:
    """Generates SQL SELECT statement from messages."""
