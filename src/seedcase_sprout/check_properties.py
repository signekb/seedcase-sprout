import seedcase_sprout.check_datapackage as cdp
from seedcase_sprout.properties import PackageProperties, ResourceProperties
from seedcase_sprout.sprout_checks.get_sprout_package_errors import (
    get_sprout_package_errors,
)
from seedcase_sprout.sprout_checks.get_sprout_resource_errors import (
    get_sprout_resource_errors,
)

# Script only constant
_RESOURCE_FIELD_PATTERN = r"resources\[\d+\]"


def check_package_properties(properties: PackageProperties) -> PackageProperties:
    """Checks that the package, not resource, `properties` match Sprout's requirements.

    Package `properties` are checked against the Data Package standard and the following
    Sprout-specific requirements:

    - Sprout-specific required fields are present.
    - Required fields are not blank.

    Args:
        properties: The package properties to check.

    Returns:
        Outputs the `properties` if all checks pass.

    Raises:
        ExceptionGroup: A group of `CheckError`s, one error per failed check.
    """
    _check_is_package_properties_type(properties)
    return _generic_check_properties(
        properties,
        ignore=[
            # Ignore checks on specific resources within the resource field.
            cdp.CheckErrorMatcher(json_path=_RESOURCE_FIELD_PATTERN),
            # Ignore missing resources.
            cdp.CheckErrorMatcher(json_path=r"resources$", validator="required"),
        ],
    )


def check_properties(properties: PackageProperties) -> PackageProperties:
    """Checks that all `properties` match Sprout's requirements.

    If the resources property hasn't been filled in yet, only package properties will
    be checked. The `properties` are checked against the Data Package standard and the
    following Sprout-specific requirements:

    - Sprout-specific required fields are present
    - Required fields are not blank

    If the resources property has been filled in, the resource properties will also
    have these checks:

    - `path` is of type string.
    - `path` includes resource name.
    - `data` is not set.

    Args:
        properties: The properties to check.

    Returns:
        Outputs the `properties` if all checks pass.

    Raises:
        ExceptionGroup: A group of `CheckError`s, one error per failed check.
    """
    _check_is_package_properties_type(properties)
    if not properties.resources:
        check_package_properties(properties)
    else:
        _generic_check_properties(properties)
    return properties


def check_resource_properties(properties: ResourceProperties) -> ResourceProperties:
    """Checks that only the resource `properties` match Sprout's requirements.

    All resource `properties` are checked against the Data Package standard and
    the following Sprout-specific requirements:

    - Sprout-specific required fields are present.
    - Required fields are not blank.
    - `path` is of type string.
    - `path` includes resource name.
    - `data` is not set.

    Args:
        properties: The resource properties to check.

    Returns:
        Outputs the `properties` if all checks pass.

    Raises:
        ExceptionGroup: A group of `CheckError`s, one error per failed check.
    """
    package_field_pattern = r"\$\.\w+$"
    _check_is_resource_properties_type(properties)
    try:
        _generic_check_properties(
            PackageProperties(resources=[properties]),
            ignore=[cdp.CheckErrorMatcher(json_path=package_field_pattern)],
        )
    # TODO: This probably is better placed in the `check-datapackage` package.
    except ExceptionGroup as error_info:
        for error in error_info.exceptions:
            if isinstance(error, cdp.CheckError):
                error.json_path = error.json_path.replace(".resources[0]", "")
        raise error_info

    return properties


def _generic_check_properties(
    properties: PackageProperties, ignore: list[cdp.CheckErrorMatcher] = []
) -> PackageProperties:
    """A generic check for Sprout-specific requirements on the Frictionless standard.

    All `properties`, excluding those in `ignore`, are checked against the Data
    Package standard as well as the following Sprout-specific requirements:

    - Sprout-specific required fields are present
    - Required fields are not blank
    - Resource `path` is of type string
    - Resource `path` includes resource name
    - Resource `data` is not set

    Args:
        properties: The full package properties to check, including resource properties.
        ignore: A list of matchers for any `CheckErrors` to ignore.

    Returns:
        Outputs the `properties` object if all checks pass.

    Raises:
        ExceptionGroup: A group of `CheckError`s, one error per failed check.
    """
    properties_dict = properties.compact_dict

    errors = cdp.check_properties(properties_dict)

    errors += get_sprout_package_errors(properties_dict)

    resources = properties_dict.get("resources")
    if isinstance(resources, list):
        for index, resource in enumerate(resources):
            if isinstance(resource, dict):
                errors += get_sprout_resource_errors(resource, index)

    errors = cdp.exclude_matching_errors(
        errors,
        [
            *ignore,
            cdp.CheckErrorMatcher(
                validator="required", json_path=rf"{_RESOURCE_FIELD_PATTERN}\.data$"
            ),
            cdp.CheckErrorMatcher(
                validator="type",
                json_path=rf"{_RESOURCE_FIELD_PATTERN}\.path$",
                message="not of type 'array'",
            ),
        ],
    )
    errors = sorted(set(errors))

    if errors:
        raise ExceptionGroup(
            f"The following checks failed on the properties:\n{properties}", errors
        )

    return properties


def _check_is_package_properties_type(properties):
    if not isinstance(properties, PackageProperties):
        raise TypeError(
            f"Expected properties to be a PackageProperties object,"
            f"but the object is {type(properties)}"
        )


def _check_is_resource_properties_type(properties):
    if not isinstance(properties, ResourceProperties):
        raise TypeError(
            f"Expected properties to be a ResourceProperties object,"
            f"but the object is {type(properties)}"
        )
