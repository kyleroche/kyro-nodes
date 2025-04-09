import requests
from griptape.artifacts import ImageArtifact
from griptape_nodes.exe_types.node_types import ControlNode
from griptape_nodes.exe_types.core_types import Parameter, ParameterMode, ParameterUIOptions
from PIL import Image
from io import BytesIO

# Define custom exception for API errors
class NasaApiError(Exception):
    pass

class NasaImageSearchNode(ControlNode):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        # Define input parameters based on the NASA API docs
        # https://images.nasa.gov/docs/images.nasa.gov_api_docs.pdf
        self.add_parameter(
            Parameter(
                name="query",
                type="str",
                tooltip="Search terms (e.g., 'apollo 11', 'mars rover'). Required.",
                allowed_modes=[ParameterMode.INPUT, ParameterMode.PROPERTY],
                default_value="apollo 11"
            )
        )
        self.add_parameter(
            Parameter(
                name="year_start",
                type="str", # API expects string YYYY
                tooltip="Start year for search range (e.g., '1969'). Optional.",
                allowed_modes=[ParameterMode.INPUT, ParameterMode.PROPERTY],
            )
        )
        self.add_parameter(
            Parameter(
                name="year_end",
                type="str", # API expects string YYYY
                tooltip="End year for search range (e.g., '1972'). Optional.",
                allowed_modes=[ParameterMode.INPUT, ParameterMode.PROPERTY],
            )
        )
        # Let's fix media_type to 'image' as we specifically want images
        # If needed later, this could become a Parameter.

        # Define output parameters
        self.add_parameter(
            Parameter(
                name="image_url",
                type="str",
                tooltip="URL of the first matching image found (preview size).",
                allowed_modes=[ParameterMode.OUTPUT],
            )
        )
        self.add_parameter(
            Parameter(
                name="image_title",
                type="str",
                tooltip="Title of the found image.",
                allowed_modes=[ParameterMode.OUTPUT],
            )
        )
        self.add_parameter(
            Parameter(
                name="image_description",
                type="str",
                tooltip="Description of the found image.",
                allowed_modes=[ParameterMode.OUTPUT],
            )
        )
        self.add_parameter(
            Parameter(
                name="error_message",
                type="str",
                tooltip="Error message if the API call fails or no image is found.",
                allowed_modes=[ParameterMode.OUTPUT],
            )
        )
        # Add new parameter for the image artifact
        self.add_parameter(
            Parameter(
                name="image",
                type="ImageArtifact",
                input_types=["ImageArtifact", "BlobArtifact"],
                tooltip="The downloaded NASA image as an ImageArtifact.",
                allowed_modes=[ParameterMode.OUTPUT, ParameterMode.PROPERTY],
                ui_options=ParameterUIOptions(
                    image_type_options=ParameterUIOptions.ImageType(expander=True, clickable_file_browser=True)
                )
            )
        )


    def process(self) -> None:
        api_url = "https://images-api.nasa.gov/search"
        query = self.parameter_values.get("query")
        year_start = self.parameter_values.get("year_start")
        year_end = self.parameter_values.get("year_end")

        # Clear previous outputs/errors
        self.parameter_output_values["image_url"] = None
        self.parameter_output_values["image_title"] = None
        self.parameter_output_values["image_description"] = None
        self.parameter_output_values["error_message"] = None
        self.parameter_output_values["image"] = None

        if not query:
            self.parameter_output_values["error_message"] = "Error: Query parameter is required."
            # Consider raising an exception or handling this differently based on desired flow control
            return

        params = {
            "q": query,
            "media_type": "image", # Fixed to image
            "page_size": 1 # We only need the first result for now
        }
        if year_start:
            params["year_start"] = year_start
        if year_end:
            params["year_end"] = year_end

        try:
            response = requests.get(api_url, params=params, timeout=10) # Added timeout
            response.raise_for_status() # Raises HTTPError for bad responses (4xx or 5xx)

            data = response.json()
            items = data.get("collection", {}).get("items", [])

            if not items:
                self.parameter_output_values["error_message"] = "No image found for the given query."
                return

            # Extract data from the first item
            first_item = items[0]
            item_data = first_item.get("data", [{}])[0]
            item_links = first_item.get("links", [])

            # Find the preview image URL
            image_url = next((link["href"] for link in item_links if link.get("rel") == "preview" and link.get("render") == "image"), None)

            if not image_url:
                 self.parameter_output_values["error_message"] = "Found result, but no preview image URL available."
                 return

            self.parameter_output_values["image_url"] = image_url
            self.parameter_output_values["image_title"] = item_data.get("title")
            self.parameter_output_values["image_description"] = item_data.get("description")

            # Now, download the actual image and create an ImageArtifact
            try:
                # Setting a User-Agent can help avoid blocks from some servers
                headers = {'User-Agent': 'GriptapeNodes-NasaImageSearchNode/1.0'}
                img_response = requests.get(image_url, stream=True, timeout=15, headers=headers)
                img_response.raise_for_status()

                image_bytes = img_response.content
                # Get content type and format
                content_type = img_response.headers.get('Content-Type', '')
                image_format = content_type.split('/')[-1].split(';')[0].strip()
                image_name = item_data.get("title", "nasa_image").replace(" ", "_")

                # Use Pillow to get dimensions
                with Image.open(BytesIO(image_bytes)) as img:
                    width, height = img.size

                # Create the ImageArtifact
                image_artifact = ImageArtifact(
                    value=image_bytes,
                    format=image_format,
                    name=image_name,
                    width=width,
                    height=height
                )

                self.parameter_output_values["image"] = image_artifact
            
            except Exception as img_err:
                self.parameter_output_values["error_message"] = f"Error downloading image: {img_err}"

        except requests.exceptions.RequestException as e:
            self.parameter_output_values["error_message"] = f"API Request Error: {e}"
        except Exception as e:
            # Catch any other unexpected errors during processing
            self.parameter_output_values["error_message"] = f"An unexpected error occurred: {e}" 