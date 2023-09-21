# imports
import os
import marvin

from dotenv import load_dotenv
from marvin import AIApplication as Bot
from rich.console import Console

# load .env
load_dotenv(os.path.expanduser("~/.birdbrain/.env"))

# hacks
# TODO: do this elsewhere?
model = "azure_openai/gpt-4-32k"
marvin.settings.llm_model = model

# TODO: hack? check if bug in Marvin
marvin.settings.azure_openai.api_key = os.getenv("MARVIN_AZURE_OPENAI_API_KEY")
marvin.settings.azure_openai.api_base = os.getenv("MARVIN_AZURE_OPENAI_API_BASE")
marvin.settings.azure_openai.deployment_name = os.getenv(
    "MARVIN_AZURE_OPENAI_DEPLOYMENT_NAME"
)
marvin.settings.azure_openai.api_type = "azure"


# classes
class AI:
    def __init__(self, name, description, tools, prompts, state):
        ai = Bot(
            name=name,
            description=description,
            tools=tools,
            additional_prompts=prompts,
            state=state,
        )

        self.ai = ai
        self.name = name
        self.tools = tools
        self.prompts = prompts
        self.description = description

        self.console = Console()

    def __call__(self, text) -> str | None:
        res = self.ai(text).content
        if self.name == "birdbrain":
            self.console.print(f"birdbrain:\n\n", style="bold violet blink", end="")
            self.console.print(res)
        else:
            return res

    def __repr__(self):
        return f"<AI {self.name}>"

    def read_excel(self, filename):
        pass

    def sql(self, text):
        import ibis
        from ibis_birdbrain.functions import choose_table_name, gen_sql_query, fix_sql_query

        con = ibis.connect("duckdb://imdb.ddb")

        tables = list(set(con.list_tables()))
        table_name = choose_table_name(text, options=tables)
        table_schema = str(con.table(table_name).schema())

        if table_name not in tables:
            raise ValueError(f"Table {table_name} not found in {tables}")
        sql = gen_sql_query(table_name, table_schema, text).strip(";")
        res = None
        try:
            res = con.table(table_name, database="imdb").sql(sql)
        except Exception as e:
            sql = fix_sql_query(table_name, table_schema, sql, str(e)).strip(";")
            try:
                res = con.table(table_name, database="imdb").sql(res)
            except Exception as e:
                raise ValueError(f"Could not execute SQL: {res} with error: {e}")

        self.console.print(f"ran SQL:\n{sql}", style="bold violet")
        return res


__all__ = ["AI", "Bot", "Console"]
