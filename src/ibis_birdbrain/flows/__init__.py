# imports
from ibis_birdbrain.tasks import Tasks
from ibis_birdbrain.logging import log
from ibis_birdbrain.messages import Messages


# classes
class Flow:
    """Ibis Birdbrain flow."""

    name: str | None
    tasks: Tasks
    description: str | None

    def __init__(
        self,
        name=None,
        tasks=None,
        description=None,
    ):
        self.name = name
        self.tasks = tasks
        self.description = description

    def __call__(self, ms: Messages) -> Messages:
        raise NotImplementedError


class Flows:
    """Ibis Birdbrain flows."""

    flows: dict[str, Flow]

    def __init__(self, flows: list[Flow] = []) -> None:
        """Initialize the flows."""
        self.flows = {f.name: f for f in flows}

    def __getitem__(self, id: str | int) -> Flow:
        """Get a flow by its name, index, or a text description."""
        if id in self.flows.keys():
            return self.flows[id]
        elif id in range(len(self.flows)):
            return self.flows[list(self.flows.keys())[id]]
        else:
            # TODO: implement LM magic
            raise KeyError

    def __len__(self) -> int:
        return len(self.flows)

    def select_flow(self, messages: Messages = None, instructions: str = None) -> Flow:
        """Select a single flow."""
        if len(self) == 1:
            flow = self[0]
            log.info(f"Selected flow: {flow.name}")
            return flow
        raise NotImplementedError


# exports
__all__ = [
    "Flow",
    "Flows",
]
