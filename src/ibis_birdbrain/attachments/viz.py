# imports
from plotly.graph_objs import Figure

from ibis_birdbrain.attachments import Attachment


# classes
class ChartAttachment(Attachment):
    """A chart attachment."""

    content: Figure

    def __init__(self, content):
        super().__init__()
        self.content = content

    def encode(self):
        ...

    def decode(self):
        ...
