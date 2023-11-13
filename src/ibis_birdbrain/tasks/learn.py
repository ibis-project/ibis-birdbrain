# imports
from ibis_birdbrain.messages import Messages, Message, Email


# tasks
def learn(m: Message) -> Messages:
    """Helps a user learn data best practices.

    Choose this task to learn data best practices
    and additional resources for learning."""
    system_messages = Messages()
    system_messages.append(
        Email(
            subject="Learning data best practices",
            body="Ibis Birdbrain is learning data best practices.",
        )
    )
    return system_messages
