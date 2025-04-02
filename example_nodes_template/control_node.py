from re import S
from typing import Any
from griptape_nodes.exe_types.node_types import ControlNode
from griptape_nodes.exe_types.core_types import Parameter, ParameterMode, ParameterUIOptions

# Control Nodes import the ControlNode class.
class ExampleControlNode(ControlNode):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.category = "DataNodes"
        self.description = "An example node with dependencies"

        # Converters should take one positional argument of any type, and can return anything!
        def capitalize_name(value:str) -> str:
            if not value:
                return value
            return value[0].upper() + value[1:]
            
        self.add_parameter(
            Parameter(
                name="first name",
                input_types=["str"],
                type="str",
                output_type="str",
                default_value = "Jane",
                tooltip="The first name of the user",
                # Converters allow you to modify the value set. You can add multiple converters, that will operate in order when a parameter value is set.
                converters=[capitalize_name]
                # If you don't specify allowed_modes, it defaults to all three modes being allowed (INPUT, OUTPUT, and PROPERTY)
            )
        )
        self.add_parameter(
            Parameter(
                name="last name",
                output_type="str",
                type="str",
                tooltip="The last name of the user",
                allowed_modes=[ParameterMode.INPUT, ParameterMode.PROPERTY],
                converters=[capitalize_name]
            )
        )
        self.add_parameter(
            Parameter(
                name="full name",
                output_type="str",
                tooltip="The full name of the user",
                allowed_modes=[ParameterMode.OUTPUT]
            )
        )
        self.add_parameter(
            Parameter(
                name="age",
                input_types=["int","float"],
                type="int",
                output_type="int",
                default_value= 30,
                tooltip="What is your age",
                # UI Options allow user to optionally set how they want their value to be displayed, based on the type. Here, I've set age to be displayed on the node as a slider. 
                # There are many types of UI Options that you can choose from. 
                ui_options=ParameterUIOptions(number_type_options=ParameterUIOptions.NumberType( slider= ParameterUIOptions.SliderWidget(min_val=1, max_val=98)))
            )
        )


    def process(self) -> None:
        # All of the current values of a parameter are stored on self.parameter_values (If they have an INPUT or PROPERTY)
        first_name = self.parameter_values["first name"]
        last_name = self.parameter_values["last name"]
        age = self.parameter_values["age"]
        # All output values should be set in self.parameter_output_values. 
        full_name = f"Your name is: {first_name} {last_name}. Your age is {age} "
        self.parameter_output_values["full name"] = full_name
        # The node is complete!