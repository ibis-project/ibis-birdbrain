# imports
from ibis_birdbrain import AI

from ibis_birdbrain.tools import tools
from ibis_birdbrain.states import BirdbrainState
from ibis_birdbrain.systems import (
    BirdbrainSystem,
    FixesSystem,
    CiteSourceSystem,
    UserPreferencesSystem,
)

# variables
state = BirdbrainState()
prompts = [FixesSystem(), CiteSourceSystem(), UserPreferencesSystem()]
description = BirdbrainSystem().content


# create bot
bot = AI(
    name=state.name, description=description, tools=tools, prompts=prompts, state=state
)
