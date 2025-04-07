from enum import Enum

# Data Package standard required fields and their types


class RequiredFieldType(str, Enum):
    """A class enumerating allowed types for required fields."""

    str = "str"
    list = "list"
    any = "any"


PACKAGE_REQUIRED_FIELDS = {
    "resources": RequiredFieldType.list,
}

PACKAGE_RECOMMENDED_FIELDS = {
    "name": RequiredFieldType.str,
    "id": RequiredFieldType.str,
    "licenses": RequiredFieldType.list,
}

RESOURCE_REQUIRED_FIELDS = {
    "name": RequiredFieldType.str,
    "path": RequiredFieldType.str,
    "data": RequiredFieldType.any,
}
