# imports
import inspect

from ibis_birdbrain.flows import Flow
from ibis_birdbrain.logging import log
from ibis_birdbrain.messages import Email, Messages
from ibis_birdbrain.attachments import (
    TableAttachment,
    CodeAttachment,
    ErrorAttachment,
    Attachments,
)

from ibis_birdbrain.tasks import Tasks
from ibis_birdbrain.tasks.sql import TextToSQLTask, ExecuteSQLTask, FixSQLTask


# flows
class DataFlow(Flow):
    """Ibis Birdbrain data flow."""

    def __init__(
        self,
        name: str = "data",
        description: str = "Ibis Birdbrain data flow",
        tasks=Tasks([TextToSQLTask(), ExecuteSQLTask(), FixSQLTask()]),
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

        # TODO: proper method for this type of stuff
        database_attachment = messages[0].attachments[0]
        data_description = database_attachment.description

        table_attachments = []
        for attachment in messages[-1].attachments:
            table_attachments.append(messages[-1].attachments[attachment])

        # initialize response messages
        response_messages = Messages()

        # call the text-to-SQL task
        task_message = Email(
            body=messages[-1].body,
            attachments=[database_attachment] + table_attachments,
            to_address=self.tasks["text-to-SQL"].name,
            from_address=self.name,
        )

        task_response = self.tasks["text-to-SQL"](task_message)
        response_messages.append(task_response)

        # check the response
        assert len(task_response.attachments) == 1
        assert isinstance(task_response.attachments[0], CodeAttachment)
        assert task_response.attachments[0].language == "sql"

        # extract the SQL attachment
        sql_attachment = task_response.attachments[0]

        # try executing
        task_message = Email(
            body="execute this SQL on the database",
            attachments=[database_attachment, sql_attachment],
            to_address=self.tasks["execute-SQL"].name,
            from_address=self.name,
        )

        task_response = self.tasks["execute-SQL"](task_message)
        response_messages.append(task_response)

        assert len(task_response.attachments) == 1

        # check the response
        if isinstance(task_response.attachments[0], TableAttachment):
            return response_messages
        elif isinstance(task_response.attachments[0], ErrorAttachment):
            # for N retries
            for i in range(self.retries):
                error_attachment = task_response.attachments[0]

                task_message = Email(
                    body="fix this SQL",
                    attachments=[error_attachment, database_attachment, sql_attachment]
                    + table_attachments,
                    to_address=self.tasks["fix-SQL"].name,
                    from_address=self.name,
                )

                # fix the SQL
                task_response = self.tasks["fix-SQL"](task_message)
                response_messages.append(task_response)

                # get the new sql_attachment
                for attachment in task_response.attachments:
                    if isinstance(
                        task_response.attachments[attachment], CodeAttachment
                    ):
                        sql_attachment = task_response.attachments[attachment]

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
