"""Core, external-facing functions of Sprout."""
# This exposes only the functions we want exposed when
# the package is imported via `from sprout.core import *`.

# Packages -----
# from .delete_package import *
# Resources -----
# from .delete_resource_raw_file import *
# from .delete_resource_data import *
# from .delete_resource_properties import *

from .build_readme_text import build_readme_text
from .create_package_properties import create_package_properties
from .create_resource_properties import create_resource_properties
from .create_resource_structure import create_resource_structure
from .edit_package_properties import edit_package_properties
from .example_package_properties import example_package_properties

# TODO: Consider having all these in one module.
from .path_package_functions import (
    path_package,
    path_packages,
    path_properties,
    path_readme,
)
from .path_resource_functions import (
    path_resource,
    path_resource_data,
    path_resource_raw,
    path_resource_raw_files,
    path_resources,
)
from .path_sprout_global import path_sprout_global
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
from .write_file import write_file
from .write_package_properties import write_package_properties

# from .extract_resource_properties import *
# from .edit_resource_properties import *
# from .write_resource_data_to_raw import *
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
    "create_package_properties",
    "edit_package_properties",
    "write_package_properties",
    "build_readme_text",
    # "delete_package",
    # Resources -----
    "create_resource_structure",
    "create_resource_properties",
    # "extract_resource_properties",
    # "edit_resource_properties",
    # "write_resource_data_to_raw",
    # "write_resource_parquet",
    "write_resource_properties",
    # "delete_resource_raw_file",
    # "delete_resource_data",
    # "delete_resource_properties",
    # Path -----
    "path_package",
    "path_packages",
    "path_properties",
    "path_readme",
    "path_resource",
    "path_resource_data",
    "path_resource_raw",
    "path_resource_raw_files",
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
