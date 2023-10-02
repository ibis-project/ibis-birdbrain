# imports
import ibis
import uuid
import marvin
import datetime

from marvin import AIApplication
from rich.console import Console

from ibis_birdbrain.utils import read_config


class Bot:
    def __init__(self, name, description, tools, prompts, state) -> None:
        ai = AIApplication(
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
        self.interactive = True

        self.console = Console()

        config = read_config(config_section="system")
        if "backend_uri" in config:
            backend_uri = config["backend_uri"]
        else:
            backend_uri = "duckdb://birdbrain.ddb"

        self.con = ibis.connect(backend_uri)

    def __call__(self, text: str) -> str | None:
        res = self.ai(text).content
        if self.interactive:
            self.console.print(f"birdbrain:\n\n", style="bold violet blink", end="")
            self.console.print(res)
        else:
            return res

    def __repr__(self):
        return f"<Bot: {self.name}>"

    def save_history(self) -> None:
        convo_id = str(uuid.uuid4())
        convo_timestamp = datetime.datetime.now()
        for message in self.ai.history.messages:
            data = {
                "convo_id": [convo_id],
                "convo_timestamp": [convo_timestamp],
                "bot_name": [self.name],
                "message_content": [message.content],
                "message_timestamp": [message.timestamp],
                "function_name": [message.name or ""],
            }
            if "history" not in self.con.list_tables():
                self.con.create_table("history", ibis.memtable(data))
            else:
                self.con.insert("history", ibis.memtable(data))
