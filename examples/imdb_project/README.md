# imdb_project

This is an example data project with IMDB data.

The data is stored in the data/ directory, typically as Delta Lake tables, though this is configurable.

Key tools used include:

- Ibis (Python data transformation)
- Delta Lake table (data storage format)
- DuckDB (query engine)
- Dagster (data workflow management)
- GitHub Actions (CI/CD)

The transformation code is in the dag/ directory.
