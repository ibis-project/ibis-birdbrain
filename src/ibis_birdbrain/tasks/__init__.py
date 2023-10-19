# imports
from ibis_birdbrain.messages import Message, Email

# tasks
def get_relevant_messages(m: Message) -> Message:
    """Get relevant messages."""
    instructions = m.body
    response = Message(
        to_address=m.from_address, from_address=m.to_address, subject=f"re: {m.subject}"
    )

    return Message(body="Getting relevant messages...")