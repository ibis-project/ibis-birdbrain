# imports
import inspect

from ibis_birdbrain.flows import Flow
from ibis_birdbrain.logging import log
from ibis_birdbrain.messages import Email, Messages
from ibis_birdbrain.attachments import (
    TableAttachment,
    SQLAttachment,
    ErrorAttachment,
    Attachments,
    DatabaseAttachment,
)

from ibis_birdbrain.tasks import Tasks
from ibis_birdbrain.tasks.sql import TextToSQLTask, ExecuteSQLTask, FixSQLTask, SearchTextTask


# flows
class DataFlow(Flow):
    """Ibis Birdbrain data flow."""

    def __init__(
        self,
        name: str = "data",
        description: str = "Ibis Birdbrain data flow",
        tasks=Tasks([
            TextToSQLTask(),
            ExecuteSQLTask(),
            FixSQLTask(),
            SearchTextTask(),
        ]),
        retries: int = 3,
    ) -> None:
        """Initialize the data flow."""
        self.retries = retries
        super().__init__(name=name, description=description, tasks=tasks)

    def __call__(self, messages: Messages) -> Messages:
        """Execute the data flow."""
        log.info("Executing the data flow")

        # TODOs:
        # - we need to construct the task messages
        # - the first message in messages has the DatabaseAttachment
        # - the last message in messages has the TableAttachments
        # - turn the body of the last message + TableAttachments into a SQLAttachment
        # - turn the DatabaseAttachment + SQLAttachment into a TableAttachment (or ErrorAttachment)
        # - finally, return the SQLAttachment + TableAttachment as results

        database_attachment = messages[0].attachments.get_attachment_by_type(DatabaseAttachment)
        table_attachments = messages[-1].attachments.get_attachment_by_type(TableAttachment)  

        # check if question is found in cached table
        search_task_response = self.tasks["search-cached-question"](messages)
        sql_attachment = search_task_response.attachments.get_attachment_by_type(SQLAttachment)
        # initialize response messages
        response_messages = Messages()
        if not sql_attachment:
            # If not existing question and sql found in the cache table
            # call the text-to-SQL task
            task_message = Email(
                body=messages[-1].body,
                attachments=[database_attachment] + list(table_attachments.attachments.values()),
                to_address=self.tasks["text-to-SQL"].name,
                from_address=self.name,
            )

            task_response = self.tasks["text-to-SQL"](task_message)
            response_messages.append(task_response)

            # check the response
            assert task_response.attachments.get_attachment_by_type(SQLAttachment) is not None

            # extract the SQL attachment
            sql_attachment = task_response.attachments.get_attachment_by_type(SQLAttachment)

        # try executing
        task_message = Email(
            body="execute this SQL on the database",
            attachments=[database_attachment, sql_attachment],
            to_address=self.tasks["execute-SQL"].name,
            from_address=self.name,
        )

        task_response = self.tasks["execute-SQL"](task_message)
        response_messages.append(task_response)

        assert len(task_response.attachments) == 2

        # check the response
        if task_response.attachments.get_attachment_by_type(TableAttachment):
            return response_messages
        elif task_response.attachments.get_attachment_by_type(ErrorAttachment):
            # for N retries
            for i in range(self.retries):
                error_attachment = task_response.attachments[0]

                task_message = Email(
                    body="fix this SQL",
                    attachments=[error_attachment, database_attachment, sql_attachment]
                    + list(table_attachments.attachments.values()),
                    to_address=self.tasks["fix-SQL"].name,
                    from_address=self.name,
                )

                # fix the SQL
                task_response = self.tasks["fix-SQL"](task_message)
                response_messages.append(task_response)

                # get the new sql_attachment
                sql_attachment = task_response.attachments.get_attachment_by_type(SQLAttachment)

                # try executing
                task_response = self.tasks["execute-SQL"](
                    Email(attachments=[database_attachment, sql_attachment])
                )
                response_messages.append(task_response)

                if isinstance(task_response.attachments[0], TableAttachment):
                    return response_messages
                elif isinstance(task_response.attachments[0], ErrorAttachment):
                    continue
                else:
                    raise ValueError
        else:
            raise ValueError

        return response_messages
