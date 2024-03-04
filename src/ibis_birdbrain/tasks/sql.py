# imports
import ibis
import marvin

from ibis_birdbrain.tasks import Task
from ibis_birdbrain.logging import log
from ibis_birdbrain.messages import Email, Message
from ibis_birdbrain.attachments import (
    Attachments,
    TableAttachment,
    CodeAttachment,
    ErrorAttachment,
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

        # get the database attachment and table attachments
        # TODO: add proper methods for this
        table_attachments = Attachments()
        database_attachment = None
        for attachment in message.attachments:
            if isinstance(message.attachments[attachment], DatabaseAttachment):
                database_attachment = message.attachments[attachment]
            elif isinstance(message.attachments[attachment], TableAttachment):
                table_attachments.append(message.attachments[attachment])

        assert len(table_attachments) > 0, "No table attachments found"
        assert database_attachment is not None, "No database attachment found"

        # generate the SQL
        sql = self.text_to_sql(
            text=message.body,
            tables=table_attachments,
            data_description=database_attachment.description,
        )
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
    def _text_to_sql(
        text: str, tables: Attachments, data_description: str, dialect: str
    ) -> str:
        """
        Generates correct, simple, and human-readable SQL based on the input
        `text`, `tables, and `data_description`, returns a SQL SELECT statement
        in the `dialect`.

        The `text` will contain a query in natural language to be answered.

        The `tables` will contain the table names and their schemas, alongside
        some metadata that can be ignored. DO NOT change the spelling or casing
        and only generate SQL for the provided tables.

        DO NOT add a LIMIT unless specifically told otherwise.

        Return (select) ALL possible columns unless specifically told otherwise.

        After joins, ensure that the columns are correctly qualified with the table name.
        """

    def text_to_sql(
        self, text: str, tables: Attachments, data_description: str, dialect="duckdb"
    ) -> str:
        """Convert text to SQL."""
        return (
            self._text_to_sql(
                text=text,
                tables=tables,
                data_description=data_description,
                dialect=dialect,
            )
            .strip()
            .strip(";")
        )


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
            attachment = TableAttachment(name="table", content=table)
        except Exception as e:
            log.error("Error executing the SQL")
            log.error("SQL: " + sql)
            log.error(e)
            attachment = ErrorAttachment(name="error", content=str(e))

        response_message = Email(
            body="execute SQL called",
            attachments=[attachment],
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

        # hackily get the database attachment, table attachments, sql attachment, and error attachment

        database_attachment = None
        table_attachments = None
        sql_attachment = None
        error_attachment = None
        for attachment in message.attachments:
            if isinstance(message.attachments[attachment], DatabaseAttachment):
                database_attachment = message.attachments[attachment]
            elif isinstance(message.attachments[attachment], TableAttachment):
                table_attachments = message.attachments[attachment]
            elif isinstance(message.attachments[attachment], CodeAttachment):
                sql_attachment = message.attachments[attachment]
            elif isinstance(message.attachments[attachment], ErrorAttachment):
                error_attachment = message.attachments[attachment]

        assert database_attachment is not None, "No database attachment found"
        assert table_attachments is not None, "No table attachments found"
        assert sql_attachment is not None, "No SQL attachment found"
        assert error_attachment is not None, "No error attachment found"

        sql = self.fix_text_to_sql(
            text=message.body,
            sql=sql_attachment.open(),
            error=error_attachment.open(),
            tables=table_attachments,
            data_description=database_attachment.description,
        )

        response_message = Email(
            body="fix SQL called",
            attachments=[CodeAttachment(language="sql", content=sql)],
            to_address=message.from_address,
            from_address=self.name,
        )
        return response_message

    @staticmethod
    @marvin.fn
    def _fix_text_to_sql(
        text: str,
        sql: str,
        error: str,
        tables: Attachments,
        data_description: str,
        dialect: str,
    ) -> str:
        """
        Fixes the `sql` to answer the `text` based on the `error`.

        Using `tables, and `data_description`, returns a SQL SELECT statement
        in the `dialect` that fixes the input SQL.

        The `text` will contain a query in natural language to be answered.

        The `tables` will contain the table names and their schemas, alongside
        some metadata that can be ignored. DO NOT change the spelling or casing
        and only generate SQL for the provided tables.

        DO NOT add a LIMIT unless specifically told otherwise.

        Return (select) ALL possible columns unless specifically told otherwise.

        After joins, ensure that the columns are correctly qualified with the table name.
        """

    def fix_text_to_sql(
        self,
        text: str,
        sql: str,
        error: str,
        tables: Attachments,
        data_description: str,
        dialect="duckdb",
    ) -> str:
        """Convert text to SQL."""
        return (
            self._fix_text_to_sql(
                text=text,
                sql=sql,
                error=error,
                tables=tables,
                data_description=data_description,
                dialect=dialect,
            )
            .strip()
            .strip(";")
        )
