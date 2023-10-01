# imports
from pydantic import BaseModel


# states
class BirdbrainState(BaseModel):
    """State of birdbrain"""

    # info about bot
    preferred_name: str = "birdbrain"
    full_name: str = "Ibis Birdbrain"
    creator: str = "Ibis developers"
    version: str = "infinity"

    # meaning of life
    meaning_of_life: int = 42

    # links to open
    ibis_docs: str = "https://www.ibis-project.org"
    ibis_github: str = "https://github.com/ibis-project/ibis"
    marvin_docs: str = "https://www.askmarvin.ai/components/overview"
    marvin_github: str = "https://github.com/prefectHQ/marvin"
    self_source_code: str = "https://github.com/ibis-project/ibis-birdbrain"

    # local files
    local_data_files: list[str] = []

    # additional links
    additional_links: list[str] = []

    # sql query hitory
    sql_history: list[str] = []

    # research info
    analysis_topic: str = ""
    analysis_description: str = ""
    analysis_abstract: str = ""
    analysis_references: list[str] = []
    analysis_analysis: str = ""
