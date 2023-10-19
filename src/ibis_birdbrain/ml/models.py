# imports
import marvin

from dotenv import load_dotenv

from pydantic import BaseModel, Field

# config
load_dotenv()
marvin.settings.llm_model = "azure_openai/gpt-4-32k"


# models
@marvin.ai_model
class Something(BaseModel):
    something: str = Field(..., description="Something")


@marvin.ai_model
class PythonDocSummary(BaseModel):
    """Summarizes a Python document."""

    description: str = Field(..., description="The description of the document.")
    summary: str = Field(..., description="The summary of the document.")
    headers: list[str] = Field(..., description="The headers of the document.")
    keywords: list[str] = Field(..., description="The keywords of the document.")
    code_snippets: list[str] = Field(
        ..., description="The code snippets of the document."
    )
    links: list[str] = Field(..., description="The links of the document.")
