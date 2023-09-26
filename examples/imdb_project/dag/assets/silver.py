# imports
from dagster import asset

from dag import functions as f


# assets
@asset
def silver_imdb_name_basics(bronze_imdb_name_basics):
    """
    Cleaned basic IMDB people names.
    """
    t = bronze_imdb_name_basics
    t = t.relabel("snake_case")
    t = f.convert_nconst_to_int(t, "nconst")
    return t


@asset
def silver_imdb_title_akas(bronze_imdb_title_akas):
    """
    Cleaned IMDB title "AKAs".
    """
    t = bronze_imdb_title_akas
    t = t.relabel("snake_case")
    t = f.convert_tconst_to_int(t, "title_id")
    return t


@asset
def silver_imdb_title_basics(bronze_imdb_title_basics):
    """
    Cleaned IMDB title basics.
    """
    t = bronze_imdb_title_basics
    t = t.relabel("snake_case")
    t = f.convert_tconst_to_int(t, "tconst")
    return t


@asset
def silver_imdb_title_crew(bronze_imdb_title_crew):
    """
    Cleaned IMDB title crew.
    """
    t = bronze_imdb_title_crew
    t = t.relabel("snake_case")
    t = f.convert_tconst_to_int(t, "tconst")
    # t = f.convert_nconst_to_int(t, "directors") # TODO: handle multiple
    # t = f.convert_nconst_to_int(t, "writers") # TODO: handle multiple
    return t


@asset
def silver_imdb_title_episode(bronze_imdb_title_episode):
    """
    Cleaned IMDB title episode.
    """
    t = bronze_imdb_title_episode
    t = t.relabel("snake_case")
    t = f.convert_tconst_to_int(t, "tconst")
    t = f.convert_tconst_to_int(t, "parent_tconst")
    return t


@asset
def silver_imdb_title_principals(bronze_imdb_title_principals):
    """
    Cleaned IMDB title principals.
    """
    t = bronze_imdb_title_principals
    t = t.relabel("snake_case")
    t = f.convert_tconst_to_int(t, "tconst")
    t = f.convert_nconst_to_int(t, "nconst")
    return t


@asset
def silver_imdb_title_ratings(bronze_imdb_title_ratings):
    """
    Cleaned IMDB title ratings.
    """
    t = bronze_imdb_title_ratings
    t = t.relabel("snake_case")
    t = f.convert_tconst_to_int(t, "tconst")
    return t
