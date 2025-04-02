from griptape_nodes.exe_types.node_types import DataNode
from griptape_nodes.exe_types.core_types import Parameter


class ExampleDataNode(DataNode):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.category = "ControlNodes"
        self.description = "An example node with dependencies"
        self.add_parameter(
            Parameter(
                name="input",
                input_types=["str","int"],
                type="str",
                default_value = 50,
                tooltip="The parameter to take strings and ints",
                allowed_modes=[ParameterMode.INPUT, ParameterMode.PROPERTY]
            )
        )
        self.add_parameter(
            Parameter(
                name="output",
                output_type="dict",
                tooltip="The output parameter",
                allowed_modes=[ParameterMode.OUTPUT]
            )
        )


    def process(self) -> None:
        # All of the current values of a parameter are stored on self.parameter_values
        # All output values should be set in self.output_values
        value = self.parameter_values["input"]
        new_dict = {"Test_key":value}
        self.parameter_output_values["input"] = new_dict