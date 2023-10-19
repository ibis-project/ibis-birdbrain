# imports
from ibis_birdbrain.utils.web import webpage_to_str, open_browser
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
        **text**: {self.content}"""
        )


class WebpageAttachment(TextAttachment):
    """A webpage attachment."""

    url: str

    def __init__(self, content=None, url="https://ibis-project.org"):
        super().__init__(url)
        self.url = url
        if content is None:
            self.content = webpage_to_str(self.url)

    def encode(self):
        ...

    def decode(self):
        ...

    def __str__(self):
        return (
            super().__str__()
            + f"""
        **url**: {self.url}"""
        )

    def open(self, browser=False):
        if browser:
            open_browser(self.url)
        else:
            return self.content
