"""
ML models for Ibis Birdbrain use Marvin AI models to
extract structured Python objects from (unstructured) text.
"""

# imports
import marvin

from dotenv import load_dotenv

from pydantic import BaseModel, Field

# config
load_dotenv()
marvin.settings.llm_model = "azure_openai/gpt-4-32k"


# models
@marvin.ai_model
class DocSummary(BaseModel):
    """Summarizes a document."""

    title: str = Field(..., description="The title of the document.")
    description: str = Field(..., description="The description of the document.")
    summary_bullets: list[str] = Field(
        ..., description="The summary of the document in bullet points."
    )
    headers: list[str] = Field(..., description="The headers of the document.")
    keywords: list[str] = Field(..., description="The keywords of the document.")
    links: list[str] = Field(..., description="The links of the document.")
    code_snippets: list[str] = Field(
        ..., description="The code snippets of the document."
    )


# TODO: probably remove, does not work well
@marvin.ai_model
class RelevantMessageExtractor(BaseModel):
    """Extracts relevant messages and attachments for constructing a message to a specific Task."""

    relevant_messages: list[str] = Field(
        ..., description="The relevant messages (list of GUIDs)"
    )
    relevant_attachments: list[str] = Field(
        ..., description="The relevant attachments (list of GUIDs)"
    )
    task_message_body: str = Field(
        ...,
        description="The task message body (str), including all instructions for successfully performing the task.",
    )
