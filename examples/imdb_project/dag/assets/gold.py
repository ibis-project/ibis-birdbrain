# imports
from dagster import asset

from dag import functions as f


# assets
@asset
def gold_imdb_ratings(silver_imdb_title_basics, silver_imdb_title_ratings):
    """
    Joined titles, ratings, and TODO more.
    """
    t = silver_imdb_title_basics.join(silver_imdb_title_ratings, "tconst", how="left")

    # filter for movies with num_votes above 50k
    # t = t.filter((t.title_type == "movie") & (t.num_votes > 50000))

    return t
