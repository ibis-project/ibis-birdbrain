# imports
from ibis_birdbrain import AI

from ibis_birdbrain.tools import tools
from ibis_birdbrain.states import ibis_birdbrainState
from ibis_birdbrain.systems import (
    ibis_birdbrainSystem,
    FixesSystem,
    CiteSourceSystem,
    UserPreferencesSystem,
)

# variables
state = ibis_birdbrainState()
prompts = [FixesSystem(), CiteSourceSystem(), UserPreferencesSystem()]
description = ibis_birdbrainSystem().content


# create bot
bot = AI(
    name=state.name, description=description, tools=tools, prompts=prompts, state=state
)
