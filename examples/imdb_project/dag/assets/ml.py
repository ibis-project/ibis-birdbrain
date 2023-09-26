# imports
from dagster import asset

from dag import functions as f


# assets
@asset  # (io_manager_key="ml_io_manager")
def ml_predict_ratings(gold_imdb_ratings):
    """
    Joined titles, ratings, and TODO more.
    """
    pass
