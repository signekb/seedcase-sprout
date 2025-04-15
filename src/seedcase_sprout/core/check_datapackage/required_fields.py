from enum import Enum


# Data Package standard required fields and their types
class RequiredFieldType(str, Enum):
    """A class enumerating allowed types for required fields."""

    str = "str"
    list = "list"
    any = "any"
