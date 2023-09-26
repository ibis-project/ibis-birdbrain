# imports
import ibis

from dagster import asset


# assets
@asset
def bronze_imdb_name_basics():
    """
    Load the basic IMDB people names from Ibis examples.
    """
    t = ibis.examples.imdb_name_basics.fetch()
    return t


@asset
def bronze_imdb_title_akas():
    """
    Load the IMDB title "AKAs" from Ibis examples.
    """
    t = ibis.examples.imdb_title_akas.fetch()
    return t


@asset
def bronze_imdb_title_basics():
    """
    Load the IMDB title basics from Ibis examples.
    """
    t = ibis.examples.imdb_title_basics.fetch()
    return t


@asset
def bronze_imdb_title_crew():
    """
    Load the IMDB title crew from Ibis examples.
    """
    t = ibis.examples.imdb_title_crew.fetch()
    return t


@asset
def bronze_imdb_title_episode():
    """
    Load the IMDB title episode from Ibis examples.
    """
    t = ibis.examples.imdb_title_episode.fetch()
    return t


@asset
def bronze_imdb_title_principals():
    """
    Load the IMDB title principals from Ibis examples.
    """
    t = ibis.examples.imdb_title_principals.fetch()
    return t


@asset
def bronze_imdb_title_ratings():
    """
    Load the IMDB title ratings from Ibis examples.
    """
    t = ibis.examples.imdb_title_ratings.fetch()
    return t
