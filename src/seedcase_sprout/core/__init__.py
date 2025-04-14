"""Core, external-facing functions of Sprout."""
# This exposes only the functions we want exposed when
# the package is imported via `from sprout.core import *`.

# Packages -----
# from .delete_package import *
# Resources -----
# from .delete_resource_batch_file import *
# from .delete_resource_data import *
# from .delete_resource_properties import *

from .as_readme_text import as_readme_text
from .create_resource_properties import create_resource_properties
from .create_resource_structure import create_resource_structure
from .examples import (
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
from .sprout_checks.check_data import check_data
from .sprout_checks.check_properties import (
    check_package_properties,
    check_properties,
    check_resource_properties,
)
from .update_package_properties import update_package_properties
from .write_file import write_file
from .write_package_properties import write_package_properties

# from .update_resource_properties import *
# from .write_resource_data_to_batch import *
# from .write_resource_parquet import *
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
    # Packages -----
    "update_package_properties",
    "write_package_properties",
    "as_readme_text",
    # "delete_package",
    # Resources -----
    "create_resource_structure",
    "create_resource_properties",
    "extract_resource_properties",
    "join_resource_batches",
    "read_resource_batches",
    # "update_resource_properties",
    # "write_resource_data_to_batch",
    # "write_resource_parquet",
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
