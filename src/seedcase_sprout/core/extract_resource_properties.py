from pathlib import Path

from frictionless import describe
from frictionless.resources import JsonResource

from seedcase_sprout.core.check_datapackage import check_resource_properties
from seedcase_sprout.core.check_is_supported_format import check_is_supported_format
from seedcase_sprout.core.internals import _check_is_file
from seedcase_sprout.core.properties import ResourceProperties


def extract_resource_properties(data_path: Path) -> ResourceProperties:
    """Extracts resource properties from a batch data file.

    This function takes the data file found at the `data_path` location and
    extracts properties from the file into a `ResourceProperties` object. This
    function is often followed by `update_resource_properties()` to fill in any
    remaining missing fields, like the `path` property field.  Usually, you use
    either this function or the `create_resource_properties()` function to
    create the initial resource properties for a specific (new) data resource.

    Args:
        data_path: The path to a batch data file of a supported format.

    Returns:
        Outputs a `ResourceProperties` object. Use `write_resource_properties()`
            to save the object to the `datapackage.json` file.
    """
    _check_is_file(data_path)
    check_is_supported_format(data_path)

    properties = describe(data_path).to_dict()

    properties.pop("dialect", None)

    if properties["format"] == "json":
        # Frictionless sets type to "json", but only "table" is accepted by
        # ResourceProperties, so we'll change the value here.
        properties["type"] = "table"

        properties["schema"] = describe(
            JsonResource(data_path).read_data(), type="schema"
        ).to_dict()

    check_resource_properties(properties)
    return ResourceProperties.from_dict(properties)
