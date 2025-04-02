from griptape_nodes.exe_types.node_types import ControlNode
from griptape_nodes.exe_types.core_types import Parameter
from griptape_nodes.retained_mode.griptape_nodes import GriptapeNodes

class ExampleDependencyNode(ControlNode):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.config = GriptapeNodes.ConfigManager()

        self.category = "ControlNodes"
        self.description = "An example node with dependencies"
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