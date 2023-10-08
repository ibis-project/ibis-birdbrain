# imports
import marvin

from pydantic import BaseModel, Field


# models
@marvin.ai_model
class ProcessDocument(BaseModel):
    """
    Document summary.
    """

    summary: str = Field(..., title="summary")
    keywords: list[str] = Field(..., title="keywords for search")
    code_snippets: list[str] = Field(..., title="code snippets")
    bullet_points: list[str] = Field(..., title="bullet points")


@marvin.ai_model
class QueryType(BaseModel):
    """
    Query type.
    """

    is_docs_query: bool = Field(..., title="is docs query")
    is_data_query: bool = Field(..., title="is data query")
    is_internet_query: bool = Field(..., title="is internet query")
