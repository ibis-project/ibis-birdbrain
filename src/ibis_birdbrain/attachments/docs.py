# imports
from ibis_birdbrain.attachments import Attachment

# classes
class TextAttachment(Attachment):
    """A text attachment."""

    content: str

    def __init__(self, content):
        super().__init__()
        self.content = content
        if (len(self.content) // 4) > 100:
            self.display_content = self.content[:50] + "..." + self.content[-50:]
        else:
            self.display_content = self.content

    def encode(self):
        ...

    def decode(self):
        ...

    def __str__(self):
        return (
            super().__str__()
            + f"""
        **text**: {self.display_content}"""
        )
