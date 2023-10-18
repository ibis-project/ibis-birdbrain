# imports
import marvin

from dotenv import load_dotenv

from pydantic import BaseModel, Field

# config
load_dotenv()
marvin.settings.llm_model = "azure_openai/gpt-4"


# models
@marvin.ai_model
class Something(BaseModel):
    something: str = Field(..., description="Something")
