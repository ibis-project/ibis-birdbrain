# imports
from marvin import ai_model
from pydantic import BaseModel, Field


# models
@ai_model
class Translate(BaseModel):
    """A translation of input text from one language to another"""

    from_: str = Field(description="The language to translate from")
    to: str = Field(description="The language to translate to")
    original: str = Field(description="The original text")
    translated: str = Field(description="The translated text")


@ai_model
class SQL(BaseModel):
    """A SQL query"""

    original: str = Field(description="The original text")
    user_intent: str = Field(description="The user's intent with the text")
    sql: str = Field(description="The SQL SELECT query to run based on the text")


@ai_model
class Summary(BaseModel):
    """A summary of input text"""

    date: str = Field(description="The date of the text")
    author: str = Field(description="The author of the text")
    description: str = Field(description="The description of the text")
    summary: str = Field(description="The one to two paragraph summary of the text")
    key_points: list[str] = Field(description="The key points of the text, if any")
    sentiment: str = Field(description="The sentiment of the text")
    sentiment_score: float = Field(description="The sentiment score of the text")
    biases: list[str] = Field(
        description="The obvious biases of the text's author, if any"
    )

    def __str__(self):
        return f"""Summary(
    date: {self.date},
    author: {self.author},
    description: {self.description},
    summary: {self.summary},
    key_points: {self.key_points},
    sentinment: {self.sentiment},
    sentinment_score:{self.sentiment_score},
    biases:{self.biases}\n)"""
