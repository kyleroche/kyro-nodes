from griptape_nodes.exe_types.node_types import ControlNode
from griptape_nodes.exe_types.core_types import Parameter

class ExampleControlNode(ControlNode):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.config = GriptapeNodes.ConfigManager()

        self.category = "Example"
        self.description = "A created Example Agent"
        self.add_parameter(
            Parameter(
                name="Parameter1",
                input_types=["str","int"],
                default_value = 50,
                tooltip="The parameter to take strings and ints",
            )
        )

    def validate_node(self) -> list[Exception] | None:
        pass

    def process(self) -> None:
        pass