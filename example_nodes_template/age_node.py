from re import S
from griptape_nodes.exe_types.node_types import DataNode
from griptape_nodes.exe_types.core_types import Parameter, ParameterMode


class Age(DataNode):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.category = "DataNodes"
        self.description = "Age Node"
        self.add_parameter(
            Parameter(
                name="age",
                input_types=["int","float"],
                type="int",
                output_type="int",
                default_value= 30,
                tooltip="What is your age",
                allowed_modes={ParameterMode.PROPERTY, ParameterMode.OUTPUT},
                # UI Options allow user to optionally set how they want their value to be displayed, based on the type. Here, I've set age to be displayed on the node as a slider. 
                # There are many types of UI Options that you can choose from. 
                ui_options={"slider":{"min_val":1,"max_val":90}}
            )
        )


    def process(self) -> None:
        # All of the current values of a parameter are stored on self.parameter_values (If they have an INPUT or PROPERTY)
        age = self.parameter_values["age"]
        # All output values should be set in self.parameter_output_values. 
        self.parameter_output_values["age"] = age
        # The node is complete!