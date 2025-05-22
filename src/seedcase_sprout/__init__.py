"""External-facing functions of Seedcase Sprout."""
# This exposes only the functions we want exposed when
# the package is imported via `from seedcase_sprout import *`.

# Packages -----
# from .delete_package import *
# Resources -----
# from .delete_resource_batch_file import *
# from .delete_resource_data import *
# from .delete_resource_properties import *

from .as_readme_text import as_readme_text
from .check_data import check_data
from .check_properties import (
    check_package_properties,
    check_properties,
    check_resource_properties,
)
from .examples import (
    ExamplePackage,
    example_data,
    example_data_all_types,
    example_package_properties,
    example_resource_properties,
    example_resource_properties_all_types,
)
from .extract_resource_properties import extract_resource_properties
from .join_resource_batches import join_resource_batches
from .paths import PackagePath
from .properties import (
    ConstraintsProperties,
    ContributorProperties,
    FieldProperties,
    LicenseProperties,
    MissingValueProperties,
    PackageProperties,
    ReferenceProperties,
    ResourceProperties,
    SourceProperties,
    TableSchemaForeignKeyProperties,
    TableSchemaProperties,
)
from .read_properties import read_properties
from .read_resource_batches import read_resource_batches
from .update_package_properties import update_package_properties
from .write_file import write_file
from .write_package_properties import write_package_properties
from .write_resource_batch import write_resource_batch

# from .update_resource_properties import *
from .write_resource_data import write_resource_data
from .write_resource_properties import write_resource_properties

__all__ = [
    # Properties -----
    "ConstraintsProperties",
    "ContributorProperties",
    "FieldProperties",
    "LicenseProperties",
    "MissingValueProperties",
    "PackageProperties",
    "ReferenceProperties",
    "ResourceProperties",
    "SourceProperties",
    "TableSchemaForeignKeyProperties",
    "TableSchemaProperties",
    "read_properties",
    # Example properties -----
    "example_package_properties",
    "example_resource_properties",
    "example_data",
    "example_data_all_types",
    "example_resource_properties_all_types",
    "ExamplePackage",
    # Packages -----
    "update_package_properties",
    "write_package_properties",
    "as_readme_text",
    # "delete_package",
    # Resources -----
    "extract_resource_properties",
    "join_resource_batches",
    "read_resource_batches",
    "write_resource_batch",
    # "update_resource_properties",
    "write_resource_data",
    "write_resource_properties",
    # "delete_resource_batch_file",
    # "delete_resource_data",
    # "delete_resource_properties",
    # Path -----
    "PackagePath",
    # Helpers -----
    # "pretty_json",
    "write_file",
    # Checks -----
    "check_package_properties",
    "check_properties",
    "check_resource_properties",
    "check_data",
]
