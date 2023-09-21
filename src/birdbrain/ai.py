# imports
from birdbrain import AI

from birdbrain.tools import tools
from birdbrain.states import BirdbrainState
from birdbrain.systems import (
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
