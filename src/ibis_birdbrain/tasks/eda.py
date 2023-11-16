# imports
from ibis_birdbrain.messages import Messages, Message, Email
from ibis_birdbrain.attachments import (
    Attachments,
    DataAttachment,
    TableAttachment,
    ChartAttachment,
    TextAttachment,
    WebpageAttachment,
)
from ibis_birdbrain.tasks import Tasks


# tasks
def eda(
    m: Message,
    sys_messages: Messages = Messages(),
    cur_depth: int = 1,
    max_depth: int = 3,
) -> (Message, Messages):
    """Perform exploratory data analysis (EDA) on data
    on behalf of the user. This includes:

        - exploring data we have access to
        - transforming data
        - visualizing data
        - basic statistical analysis
        - basic prose summary of data

    Choose this task to perform exploratory data analysis (EDA)
    on data on behalf of the user."""

    # initialize system
    if len(sys_messages) == 0:
        sys_messages.append(m)

    # set eda_tasks
    eda_tasks = {
        data_to_tables.__doc__: data_to_tables,
        transform_data.__doc__: transform_data,
        visualize_data.__doc__: visualize_data,
        summarize_data.__doc__: summarize_data,
    }
    eda_tasks = Tasks(eda_tasks)

    # select task
    task = eda_tasks.select(sys_messages, text=m.body)

    # run task
    o = task(m)

    # append message to messages
    sys_messages.append(o)

    # recurse
    if cur_depth < max_depth:
        o, sys_messages = eda(
            o, sys_messages, cur_depth=cur_depth + 1, max_depth=max_depth
        )

    # return
    return o, sys_messages


def transform_data(m: Message) -> Message:
    """Not implemented"""
    return m


def visualize_data(m: Message) -> Message:
    """Not implemented"""
    return m


def summarize_data(m: Message) -> Message:
    """Not implemented"""
    return m


def data_to_tables(m: Message) -> Message:
    """Converts data attachments to table attachments."""
    data_attachments = []
    for a in m.attachments:
        if isinstance(m.attachments[a], DataAttachment):
            data_attachments.append(m.attachments[a])
        elif isinstance(m.attachments[a], TableAttachment):
            data_attachments.append(m.attachments[a].content)
    table_attachments = []
    for d in data_attachments:
        for t in d.con.list_tables():
            table_attachments.append(
                TableAttachment(
                    name=t,
                    content=d.con.table(t),
                )
            )

    o = Email(
        subject="Data to tables",
        body="Ibis Birdbrain is converting data to tables.",
        attachments=table_attachments,
    )

    return o
