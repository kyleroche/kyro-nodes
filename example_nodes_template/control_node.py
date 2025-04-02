from griptape_nodes.exe_types.node_types import ControlNode
from griptape_nodes.exe_types.core_types import Parameter, ParameterUIOptions

# Define your node as a class. 
# This can either inherit ControlNode or DataNode.
class ExampleControlNode(ControlNode):
    
    # Initialize your node. This should set all fields and add all parameters to the node.
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.category = "ControlNodes"
        self.description = "A created Example Control Agent"

        # ParameterUIOptions: 

        self.add_parameter(
            Parameter(
                name="ExampleInputParameter",
                input_types=["str","int"],
                type="str",
                default_value = 50,
                tooltip="The parameter to take strings and ints",
                ui_options=ParameterUIOptions
            )
        )

    def validate_node(self) -> list[Exception] | None:
        pass

    def process(self) -> None:
        """This method establishes your """
        pass