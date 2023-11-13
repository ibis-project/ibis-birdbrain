# imports
from ibis_birdbrain.messages import Messages, Message, Email
from ibis_birdbrain.attachments import (
    DatabaseAttachment,
    TableAttachment,
    ChartAttachment,
    TextAttachment,
    WebpageAttachment,
)


# tasks
def eda(m: Message) -> Messages:
    """Perform exploratory data analysis (EDA) on data
    on behalf of the user. This includes:

        - exploring data we have access to
        - transforming data
        - visualizing data
        - basic statistical analysis
        - basic prose summary of data

    Choose this task to perform exploratory data analysis (EDA)
    on data on behalf of the user."""
    # what tables are needed? check for clarity...?
    #   perhaps check if table attachments (add method for that)
    #   exist, otherwise figure out the database and run that ->
    #   intermediary message (need to deal w/ that)

    # do the table(s) need to be transformed? if so, how?
    # run that and get results as another message?

    # are visualizations needed?
    # ...

    system_messages = Messages()
    system_messages.append(
        Email(
            subject="Analyzing data",
            body="Ibis Birdbrain is analyzing data.",
        )
    )
    return system_messages


def transform_data(m: Message) -> Message:
    """Not implemented"""
    ...


def visualize_data(m: Message) -> Message:
    """Not implemented"""
    ...
