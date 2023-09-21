# imports
import ibis

# create connection to duckdb
con = ibis.connect("duckdb://imdb.ddb")

# fetch data from ibis examples
imdb_name_basics = ibis.examples.imdb_name_basics.fetch()
imdb_title_akas = ibis.examples.imdb_title_akas.fetch()
imdb_title_basics = ibis.examples.imdb_title_basics.fetch()
imdb_title_crew = ibis.examples.imdb_title_crew.fetch()
imdb_title_episode = ibis.examples.imdb_title_episode.fetch()
imdb_title_principals = ibis.examples.imdb_title_principals.fetch()
imdb_title_ratings = ibis.examples.imdb_title_ratings.fetch()

# create tables in con
con.create_table("imdb_name_basics", imdb_name_basics.to_pyarrow(), overwrite=True)
con.create_table("imdb_title_akas", imdb_title_akas.to_pyarrow(), overwrite=True)
con.create_table("imdb_title_basics", imdb_title_basics.to_pyarrow(), overwrite=True)
con.create_table("imdb_title_crew", imdb_title_crew.to_pyarrow(), overwrite=True)
con.create_table("imdb_title_episode", imdb_title_episode.to_pyarrow(), overwrite=True)
con.create_table(
    "imdb_title_principals", imdb_title_principals.to_pyarrow(), overwrite=True
)
con.create_table("imdb_title_ratings", imdb_title_ratings.to_pyarrow(), overwrite=True)
