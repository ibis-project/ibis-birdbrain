# imports
from plotly.graph_objs import Figure

from ibis_birdbrain.attachments import Attachment


# classes
class ChartAttachment(Attachment):
    """A chart attachment."""

    content: Figure

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
    **chart**:\n{self.content}"""
        )
