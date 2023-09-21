# imports
from pydantic import BaseModel


# states
class ibis_birdbrainState(BaseModel):
    """State of ibis_birdbrain"""

    # info about bot
    name: str = "ibis_birdbrain"
    creator: str = "Ibis developers"
    version: str = "infinity"

    # links to open
    ibis_docs: str = "https://www.ibis-project.org"
    ibis_github: str = "https://github.com/ibis-project/ibis"
    marvin_docs: str = "https://www.askmarvin.ai/components/overview"
    marvin_github: str = "https://github.com/prefectHQ/marvin"
    self_source_code: str = "https://github.com/ibis-project/ibis-ibis_birdbrain"

    # additional links
    additional_links: list[str] = []

    # research info
    analysis_topic: str = "data"
    analysis_description: str = ""
    analysis_abstract: str = ""
    analysis_references: list[str] = []
    analysis_analysis: str = ""
