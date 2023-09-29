# imports
import os
import marvin

from dotenv import load_dotenv

# load .env
load_dotenv(os.path.expanduser("~/.birdbrain/.env"))

# hacks
# TODO: do this elsewhere?
model = "azure_openai/gpt-4"
marvin.settings.llm_model = model

# TODO: hack? check if bug in Marvin
marvin.settings.azure_openai.api_key = os.getenv("MARVIN_AZURE_OPENAI_API_KEY")
marvin.settings.azure_openai.api_base = os.getenv("MARVIN_AZURE_OPENAI_API_BASE")
marvin.settings.azure_openai.deployment_name = os.getenv(
    "MARVIN_AZURE_OPENAI_DEPLOYMENT_NAME"
)
marvin.settings.azure_openai.api_type = "azure"
