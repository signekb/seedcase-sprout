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
from .example_package_properties import example_package_properties
from .extract_resource_properties import extract_resource_properties

# TODO: Consider having all these in one module.
from .path_global import (
    path_package,
    path_packages,
    path_sprout_global,
)
from .path_local import (
    path_properties,
    path_readme,
    path_resource,
    path_resource_batch,
    path_resource_batch_files,
    path_resource_data,
    path_resources,
)
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
from .sprout_checks.check_package_properties import check_package_properties
from .sprout_checks.check_properties import check_properties
from .sprout_checks.check_resource_properties import check_resource_properties
from .update_package_properties import update_package_properties
from .write_file import write_file
from .write_package_properties import write_package_properties

# from .edit_resource_properties import *
# from .write_resource_data_to_batch import *
# from .write_resource_parquet import *
from .write_resource_properties import write_resource_properties

# Helpers -----
# from .pretty_json import *

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
    # Example properties -----
    "example_package_properties",
    # Packages -----
    "update_package_properties",
    "edit_package_properties",
    "write_package_properties",
    "as_readme_text",
    # "delete_package",
    # Resources -----
    "create_resource_structure",
    "create_resource_properties",
    "extract_resource_properties",
    # "edit_resource_properties",
    # "write_resource_data_to_batch",
    # "write_resource_parquet",
    "write_resource_properties",
    # "delete_resource_batch_file",
    # "delete_resource_data",
    # "delete_resource_properties",
    # Path -----
    "path_package",
    "path_packages",
    "path_properties",
    "path_readme",
    "path_resource",
    "path_resource_data",
    "path_resource_batch",
    "path_resource_batch_files",
    "path_resources",
    "path_sprout_global",
    # Helpers -----
    # "pretty_json",
    "write_file",
    # Checks -----
    "check_package_properties",
    "check_properties",
    "check_resource_properties",
]
