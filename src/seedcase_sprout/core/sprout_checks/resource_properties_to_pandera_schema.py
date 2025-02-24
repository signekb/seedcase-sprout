import pandera.polars as pa

from seedcase_sprout.core.get_nested_attr import get_nested_attr
from seedcase_sprout.core.properties import FieldProperties, ResourceProperties
from seedcase_sprout.core.sprout_checks.get_pandera_checks import (
    get_pandera_checks,
)
from seedcase_sprout.core.sprout_checks.get_polars_data_type import (
    get_polars_data_type,
)


def resource_properties_to_pandera_schema(
    resource_properties: ResourceProperties,
) -> pa.DataFrameSchema:
    """Converts a set of resource properties to a Pandera schema.

    Args:
        resource_properties: The resource properties to convert.

    Returns:
        The resulting Pandera schema.
    """
    fields: list[FieldProperties] = get_nested_attr(
        resource_properties,
        "schema.fields",
        default=[],
    )

    columns = {
        field.name: pa.Column(
            dtype=get_polars_data_type(field.type),
            checks=get_pandera_checks(field),
            nullable=not get_nested_attr(field, "constraints.required", default=False),
            coerce=True,
        )
        for field in fields
    }

    return pa.DataFrameSchema(columns, strict=True)
