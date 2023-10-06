# imports
from ibis_birdbrain.ai import Bot

from ibis_birdbrain.states.tpch3000 import BirdbrainTPCHState
from ibis_birdbrain.systems.tpch3000 import TPCHSystem
from ibis_birdbrain.systems.default import (
    BirdbrainSystem,
    FixesSystem,
    CiteSourcesSystem,
    UserPreferencesSystem,
)

from ibis_birdbrain.tools.internet import (
    open_browser,
    search_internet,
    webpage_to_str,
)
from ibis_birdbrain.tools.text import summarize_text, translate_text
from ibis_birdbrain.tools.code import (
    text_to_python,
    fix_python_error,
    run_python_code,
    python_function_to_udf,
)
from ibis_birdbrain.tools.filesystem import read_file, list_files_and_dirs, write_file
from ibis_birdbrain.tools.tpch3000 import (
    list_tables,
    get_table_schemas,
    generate_sql,
    execute_sql,
    generate_tpch_data,
    write_tables_to_parquet,
)
from ibis_birdbrain.tools.advanced import (
    read_files_and_summarize,
    read_webpage_and_summarize,
)
from ibis_birdbrain.tools.github import use_github_cli

# bot setup
state = BirdbrainTPCHState()
prompts = [FixesSystem(), CiteSourcesSystem(), UserPreferencesSystem()]
description = TPCHSystem().content


# bot tools
tools = [
    # internet
    open_browser,
    search_internet,
    webpage_to_str,
    # text
    summarize_text,
    translate_text,
    # code
    text_to_python,
    fix_python_error,
    run_python_code,
    python_function_to_udf,
    # Ibis
    list_tables,
    get_table_schemas,
    generate_sql,
    execute_sql,
    generate_tpch_data,
    write_tables_to_parquet,
    # advanced
]

# bot
bot = Bot(
    name=state.preferred_name,
    description=description,
    tools=tools,
    prompts=prompts,
    state=state,
)
