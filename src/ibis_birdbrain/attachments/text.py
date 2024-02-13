# imports
from ibis_birdbrain.utils.web import webpage_to_str, open_browser
from ibis_birdbrain.utils.strings import estimate_tokens, shorten_str
from ibis_birdbrain.attachments import Attachment


# classes
class TextAttachment(Attachment):
    """A text attachment."""

    content: str

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if estimate_tokens(self.content) > 200:
            self.display_content = (
                shorten_str(self.content, 50)
                + shorten_str(self.content[::-1], 50)[::-1]
            )
        else:
            self.display_content = self.content

    def encode(self):
        ...

    def decode(self):
        ...

    # def __str__(self):
    #     return (
    #         super().__str__()
    #         + f"""
    # **text**:\n{self.content}"""
    #     )


class WebpageAttachment(Attachment):
    """A webpage attachment."""

    content: str
    url: str

    def __init__(self, *args, url="https://ibis-project.org", **kwargs):
        super().__init__(*args, **kwargs)
        self.url = url
        if self.content is None:
            self.content = webpage_to_str(self.url)
        if estimate_tokens(self.content) > 100:
            self.display_content = (
                shorten_str(self.content, 50)
                + shorten_str(self.content[::-1], 50)[::-1]
            )
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
    **url**: {self.url}
    **content**:\n{self.display_content}"""
        )

    def open(self, browser=False):
        if browser:
            open_browser(self.url)
        else:
            return self.url


class CodeAttachment(TextAttachment):
    """A code attachment."""

    content: str
    language: str

    def __init__(self, language="python", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.language = language

    def encode(self):
        ...

    def decode(self):
        ...

    def __str__(self):
        return (
            super().__str__()
            + f"""
    **language**: {self.language}
    **code**:\n{self.content}"""
        )


class ErrorAttachment(TextAttachment):
    """An error attachment."""

    content: str

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def encode(self):
        ...

    def decode(self):
        ...

    def __str__(self):
        return (
            super().__str__()
            + f"""
    **error**:\n{self.content}"""
        )
