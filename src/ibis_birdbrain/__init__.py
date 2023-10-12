# imports
import logging as log

from ibis_birdbrain.bot import Bot, bot

# configure logging level
log.basicConfig(
    level=log.INFO,
)

__all__ = ["Bot", "bot"]
