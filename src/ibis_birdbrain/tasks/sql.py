# imports
import ibis
import marvin

from Levenshtein import ratio

from ibis_birdbrain.tasks import Task
from ibis_birdbrain.logging import log
from ibis_birdbrain.messages import Email, Message, Messages
from ibis_birdbrain.attachments import (
    Attachments,
    TableAttachment,
    SQLAttachment,
    ErrorAttachment,
    DatabaseAttachment,
)


@ibis.udf.scalar.python
def levenshtein_ratio(text1: str, text2: str) -> float:
    return ratio(text1, text2)

# tasks
class SearchTextTask(Task):
    """Ibis Birdbrain task to search cached text and SQL pair."""

    def __init__(
        self, name: str = "search-cahced-question", description: str = "Ibis Birdbrain search task"
    ) -> None:
        """Initialize the searchtask."""
        super().__init__(name=name, description=description)

    def __call__(self, messages: Messages) -> Message:
        """Search text task."""
        log.info("Search text task.")

        try:
            cached_table = messages[0].attachments.get_attachment_by_type(TableAttachment)[0].open()
            question = messages[-1].body
            matched_res = cached_table.mutate(
                similarity=levenshtein_ratio(ibis._.question, question)
            ).filter(
                ibis._.similarity > 0.75 # Threshold
            ).order_by(
                ibis._.similarity.desc()
            ).limit(1).to_pandas()

            log.info(f"similarity = {matched_res.iloc[0]['similarity']}")
            log.info(f"sql = {matched_res.iloc[0]['sql']}")

            sql_attachment = SQLAttachment(
                dialect=matched_res.iloc[0]['dialect'],
                content=matched_res.iloc[0]['sql']
            )
            
            return Email(
                body="search cached question called",
                attachments=[sql_attachment],
                to_address=messages[-1].from_address,
                from_address=self.name,
            )
        except Exception as e:
            return Email(
                body=f"No similar question found",
                to_address=messages[-1].from_address,
                from_address=self.name,
            )
    

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
        dialect = "duckdb"
        for attachment in message.attachments:
            if isinstance(message.attachments[attachment], DatabaseAttachment):
                database_attachment = message.attachments[attachment]
                dialect = database_attachment.open().name
            elif isinstance(message.attachments[attachment], TableAttachment):
                table_attachments.append(message.attachments[attachment])

        assert len(table_attachments) > 0, "No table attachments found"
        assert database_attachment is not None, "No database attachment found"

        # generate the SQL
        sql = self.text_to_sql(
            text=message.body,
            tables=table_attachments,
            data_description=database_attachment.description,
            dialect=dialect,
        )
        sql_attachment = SQLAttachment(dialect=dialect, content=sql)

        # generate the response message
        response_message = Email(
            body="text to sql called",
            attachments=[sql_attachment],
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
        sql_attachment = message.attachments.get_attachment_by_type(SQLAttachment)
        database_attachment = message.attachments.get_attachment_by_type(DatabaseAttachment)

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
            attachments=[attachment, sql_attachment],
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

        database_attachment = message.attachments.get_attachment_by_type(DatabaseAttachment)
        table_attachments = message.attachments.get_attachment_by_type(TableAttachment)
        sql_attachment = message.attachments.get_attachment_by_type(SQLAttachment)
        error_attachment = message.attachments.get_attachment_by_type(ErrorAttachment)

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
            dialect=sql_attachment.dialect
        )

        response_message = Email(
            body="fix SQL called",
            attachments=[SQLAttachment(dialect=sql_attachment.dialect, content=sql)],
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
