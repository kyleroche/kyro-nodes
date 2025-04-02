from griptape_nodes.exe_types.node_types import DataNode
from griptape_nodes.exe_types.core_types import Parameter

class ExampleDataNode(DataNode):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.config = GriptapeNodes.ConfigManager()

        self.category = "Agent"
        self.description = "Create an agent and run it."
        self.add_parameter(
            Parameter(
                name="agent",
                allowed_types=["Agent"],
                tooltip="",
            )
        )

    # Only requires a valid OPENAI_API_KEY
    def validate_node(self) -> list[Exception] | None:
        # Items here are openai api key
        pass

    def process(self) -> None:
        # Get api key
        pass
