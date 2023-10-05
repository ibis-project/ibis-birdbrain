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
    reflex_docs: str = "https://reflex.dev/docs/components/overview"
    reflex_github: str = "https://github.com/reflex-dev/reflex"
    birdbrain_docs: str = "https://ibis-project.github.io/ibis-birdbrain"
    birdbrain_github: str = "https://github.com/ibis-project/ibis-birdbrain"

    local_data_files: list[str] = []

    # additional links
    additional_links: list[str] = []
