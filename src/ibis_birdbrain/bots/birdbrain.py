# imports
from ibis_birdbrain.ai import Bot

from ibis_birdbrain.states.default import BirdbrainState
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
from ibis_birdbrain.tools.eda import (
    list_tables,
    get_table_schemas,
    generate_and_execute_sql,
    read_delta_table,
    read_excel_file,
)
from ibis_birdbrain.tools.advanced import (
    read_files_and_summarize,
    read_webpage_and_summarize,
)
from ibis_birdbrain.tools.github import use_github_cli

# bot setup
state = BirdbrainState()
prompts = [FixesSystem(), CiteSourcesSystem(), UserPreferencesSystem()]
description = BirdbrainSystem().content


# bot tools
tools = [
    # internet
    open_browser,
    search_internet,
    webpage_to_str,
    # text
    summarize_text,
    translate_text,
    # filesystem
    read_file,
    list_files_and_dirs,
    write_file,
    # code
    text_to_python,
    fix_python_error,
    run_python_code,
    python_function_to_udf,
    # Ibis
    list_tables,
    get_table_schemas,
    generate_and_execute_sql,
    read_delta_table,
    read_excel_file,
    # advanced
    read_files_and_summarize,
    read_webpage_and_summarize,
    # github
    # use_github_cli,
]

# bot
bot = Bot(
    name=state.preferred_name,
    description=description,
    tools=tools,
    prompts=prompts,
    state=state,
)