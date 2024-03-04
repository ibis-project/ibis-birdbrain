# imports
import ibis
import marvin

from ibis_birdbrain.tasks import Task
from ibis_birdbrain.logging import log
from ibis_birdbrain.messages import Email, Message
from ibis_birdbrain.attachments import (
    TableAttachment,
    CodeAttachment,
    DatabaseAttachment,
)


# tasks
class TextToSQLTask(Task):
    """Ibis Birdbrain task to turn text into SQL."""

    def __init__(
        self, name: str = "text-to-SQL", description: str = "Ibis Birdbrain SQL task"
    ) -> None:
        """Initialize the SQL task."""
        super().__init__(name=name, description=description)

    def __call__(self, message: Message) -> Message:
        """Text to SQL task."""
        log.info("Text to SQL task")

        # generate the SQL
        sql = self.text_to_sql(message.body)
        code_attachment = CodeAttachment(language="sql", content=sql)

        # generate the response message
        response_message = Email(
            body="text to sql called",
            attachments=[code_attachment],
            to_address=message.from_address,
            from_address=self.name,
        )
        return response_message

    @staticmethod
    @marvin.fn
    def _text_to_sql(text: str, dialect: str) -> str:
        """Based on the input `text`, returns a SQL SELECT statement in the `dialect`.

        The `text` will contain:
            - a query in natural language
            - a description of the data
            - a list of TableAttachments, with the table names and schemas

        Use ONLY the provided tables and their schemas to generate the query.

        DO NOT change the spelling or casing of table or column names.

        Return (select) ALL columns unless specifically told otherwise.

        Generates correct, simple, and human-readable SQL.
        """

    def text_to_sql(self, text: str, dialect="duckdb") -> str:
        """Convert text to SQL."""
        return self._text_to_sql(text=text, dialect=dialect).strip().strip(";")


class ExecuteSQLTask(Task):
    """Ibis Birdbrain task to execute SQL."""

    def __init__(
        self, name: str = "execute-SQL", description: str = "Ibis Birdbrain SQL task"
    ) -> None:
        """Initialize the SQL task."""
        super().__init__(name=name, description=description)

    def __call__(self, message: Message) -> Message:
        """Execute the SQL task."""
        log.info("Executing the SQL task")

        # get the database attachment and sql attachments
        # TODO: add proper methods for this

        for attachment in message.attachments:
            if isinstance(message.attachments[attachment], CodeAttachment):
                sql_attachment = message.attachments[attachment]
            elif isinstance(message.attachments[attachment], DatabaseAttachment):
                database_attachment = message.attachments[attachment]

        con = database_attachment.open()
        sql = sql_attachment.open()

        # execute the SQL
        try:
            table = con.sql(sql)
        except Exception as e:
            table = None
            log.error("Error executing the SQL")
            log.error("SQL: " + sql)
            log.error(e)

        response_message = Email(
            body="execute SQL called",
            attachments=[TableAttachment(name="table", content=table)],
            to_address=message.from_address,
            from_address=self.name,
        )
        return response_message


class FixSQLTask(Task):
    """Ibis Birdbrain task to fix SQL."""

    def __init__(
        self, name: str = "fix-SQL", description: str = "Ibis Birdbrain SQL task"
    ) -> None:
        """Initialize the SQL task."""
        super().__init__(name=name, description=description)

    def __call__(self, message: Message) -> Message:
        """Fix the SQL task."""
        log.info("Fixing the SQL task")
        response_message = Email()
        return response_message
