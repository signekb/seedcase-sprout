# NOTE: This content is modified from the auto-generated
# `generate_properties/generated_properties.py` file. Update the auto-generated
# properties file to add more dataclasses and move them into this file.


from abc import ABC
from dataclasses import asdict, dataclass, field
from typing import Any, Literal


class Properties(ABC):
    """An abstract base class for all *Properties classes holding common logic."""

    @property
    def asdict(self) -> dict:
        """Produces a dictionary representation of the object.

        Returns:
            The object as a dictionary.
        """
        return asdict(self)


@dataclass
class ContributorProperties(Properties):
    """The people or organizations who contributed to this data package.

    Attributes:
        title (str): The name of the contributor.
        path (str): A fully qualified URL pointing to a relevant
            location online for the contributor.
        email (str): An email address.
        given_name (str): A string containing the name a person has been
            given, if the contributor is a person.
        family_name (str): A string containing the familial name that a person
            inherits, if the contributor is a person.
        organization (str): An organizational affiliation for this contributor.
        roles (list[str]): An array of strings describing the roles of the contributor.
    """

    title: str = ""
    path: str = ""
    email: str = ""
    given_name: str = ""
    family_name: str = ""
    organization: str = ""
    roles: list[str] = field(default_factory=list)


@dataclass
class LicenseProperties(Properties):
    """The license(s) under which the package or resource is provided.

    Attributes:
        name (str): Must be an Open Definition license identifier,
            see http://licenses.opendefinition.org/
        path (str): A fully qualified URL, or a POSIX file path.
        title (str): A human-readable title.
    """

    name: str = ""
    path: str = ""
    title: str = ""


@dataclass
class SourceProperties(Properties):
    """The raw sources for this data package.

    Attributes:
        title (str): The title of the source (e.g. document or organization).
        path (str): A fully qualified URL, or a POSIX file path.
        email (str): An email address.
        version (str): The version of the source.
    """

    title: str = ""
    path: str = ""
    email: str = ""
    version: str = ""


# The `r"""` string is used to avoid escaping backslashes in the `null_sequence`
# attribute.
@dataclass
class TableDialectProperties(Properties):
    r"""Table dialect describes how tabular data is stored in a file.

    It supports delimited text files like CSV, semi-structured formats like JSON
    and YAML, and spreadsheets like Microsoft Excel.

    Attributes:
        header (bool): Specifies if the file includes a header row,
            always as the first row in the file.
        header_rows (list[int]): Specifies the row numbers for the header.
        header_join (str): Specifies how multiline-header files have to join
            the resulting header rows.
        comment_rows (list[int]): Specifies what rows have to be omitted from the data.
        comment_char (str): Specifies that any row beginning with
            this one-character string, without preceding whitespace, causes the
            entire line to be ignored.
        delimiter (str): A character sequence to use as the field separator.
        line_terminator (str): Specifies the character sequence that
            must be used to terminate rows.
        quote_char (str): Specifies a character to use for quoting in
            case the `delimiter` is used inside a data cell.
        double_quote (bool): Controls the handling of `quote_char` inside
            data cells. If true, two consecutive quotes are interpreted as one.
        escape_char (str): Specifies a one-character string to use as
            the escape character. Mutually exclusive with `quote_char`.
        null_sequence (str): Specifies the null sequence, for example, `\N`.
        skip_initial_space (bool): Specifies the interpretation of
            whitespace immediately following a delimiter. If false, whitespace
            immediately after a delimiter should be treated as part of the
            subsequent field.
        property (str): Specifies where a data array is located in the data structure.
        item_type (Literal['array', 'object']): Specifies whether `property`
            contains an array of arrays or an array of objects.
        item_keys (list[str]): Specifies the keys for extracting rows from
            data arrays where `item_type` is `object`.
        sheet_number (int): Specifies the sheet number of a table in a spreadsheet
            file.
        sheet_name (str): Specifies the sheet name of a table in a spreadsheet file.
        table (str): Specifies the name of a table in a database.
    """

    header: bool = True
    header_rows: list[int] = field(default_factory=lambda: [1])
    header_join: str = " "
    comment_rows: list[int] = field(default_factory=lambda: [1])
    comment_char: str = ""
    delimiter: str = ","
    line_terminator: str = "\r\n"
    quote_char: str = '"'
    double_quote: bool = True
    escape_char: str = ""
    null_sequence: str = ""
    skip_initial_space: bool = False
    property: str = ""
    item_type: Literal["array", "object"] = "array"
    item_keys: list[str] = field(default_factory=list)
    sheet_number: int = 1
    sheet_name: str = ""
    table: str = ""


@dataclass
class ReferenceProperties(Properties):
    """The destination part of a foreign key.

    Attributes:
        resource: (str | None): The name of the resource within the current data
            package where the `fields` are located.
        fields: (list[str] | None): An array of strings of the same length as
            `TableSchemaForeignKeyProperties.fields`, specifying the field (or fields)
            that form the destination part of the foreign key.
    """

    resource: str | None = None
    fields: list[str] | None = None


@dataclass
class TableSchemaForeignKeyProperties(Properties):
    """A foreign key in a table schema.

    A foreign key is a reference where values in a field (or fields) on the table
    ("resource" in data package terminology) described by the table schema connect to
    values in a field (or fields) on this or a separate table (resource).

    Attributes:
        fields (list[str] | None): An array of strings specifying the field (or
            fields) on this resource that form the source part of the foreign key.
        reference (ReferenceProperties | None): An object specifying the
            destination part of the foreign key.
    """

    fields: list[str] | None = None
    reference: ReferenceProperties | None = None


@dataclass
class MissingValueProperties(Properties):
    """Values that, when encountered in the source, should be considered as not present.

    Attributes:
        value (str | None): String representing the missing value.
        label (str | None): A human-readable label for the missing value.
    """

    value: str | None = None
    label: str | None = None


# Allowed types for a field in a table schema.
FieldType = Literal[
    "string",
    "number",
    "integer",
    "boolean",
    "object",
    "array",
    "list",
    "datetime",
    "date",
    "time",
    "year",
    "yearmonth",
    "duration",
    "geopoint",
    "geojson",
    "any",
]


@dataclass
class ConstraintsProperties(Properties):
    """A class that expresses constraints for validating field values.

    Attributes:
        required (bool | None): Indicates whether a property must have a
            value for each instance.
        unique (bool | None): When `true`, each value for the property
            must be unique.
        pattern (str | None): A regular expression pattern to test each
            value of the property against, where a truthy response indicates
            validity.
        enum (list | None): The value of the field must exactly match one of
            the values in the `enum` array.
        min_length (int | None): An integer that specifies the minimum
            length of a value.
        max_length (int | None): An integer that specifies the maximum
            length of a value.
        minimum (str | float | int | None): Specifies a minimum value for a field.
        maximum (str | float | int | None): Specifies a maximum value for a field.
        exclusive_minimum (str | float | int | None): Specifies an exclusive minimum
            value for a field.
        exclusive_maximum (str | float | int | None): Specifies an exclusive maximum
            value for a field.
        json_schema (dict[str, Any] | None): A valid JSON schema object to
            validate field values. If a field value conforms to the provided
            JSON schema then this field value is valid.
    """

    required: bool | None = None
    unique: bool | None = None
    pattern: str | None = None
    enum: list | None = None
    min_length: int | None = None
    max_length: int | None = None
    minimum: str | float | int | None = None
    maximum: str | float | int | None = None
    exclusive_minimum: str | float | int | None = None
    exclusive_maximum: str | float | int | None = None
    json_schema: dict[str, Any] | None = None


@dataclass
class FieldProperties(Properties):
    """A field in a table schema.

    Provides human-readable documentation as well as additional information that can
    be used to validate the field or create a user interface for data entry.

    Attributes:
        name (str | None): A name for this field. Must be unique amongst other field
            names in this table schema.
        title (str | None): A human readable label or title for this field.
        type (FieldType | None): The data type of this field.
        format (str | None): The format for this field.
        description (str | None): A text description for this field.
        example (str | None): An example value for this field.
        constraints (ConstraintsProperties | None): The constraints applicable to
            this field.
        categories (list[str] | list[int] | None): A finite set of possible values
            for this field.
        categories_ordered (bool | None): Specifies whether the order of appearance
            of the values in the `categories` property should be regarded as their
            natural order.
        missing_values (list[str] | list[MissingValueProperties] | None): Values that,
            when encountered in the field, should be considered as not present. Takes
            precedence over the schema-level property.
    """

    name: str | None = None
    title: str | None = None
    type: FieldType | None = None
    format: str | None = "default"
    description: str | None = None
    example: str | None = None
    constraints: ConstraintsProperties | None = None
    categories: list[str] | list[int] | None = None
    categories_ordered: bool | None = None
    missing_values: list[str] | list[MissingValueProperties] | None = field(
        default_factory=lambda: [""]
    )


# Allowed strategies for matching fields in the table schema to fields the data source.
FieldsMatchType = Literal["exact", "equal", "subset", "superset", "partial"]


@dataclass
class TableSchemaProperties(Properties):
    """A table schema for a data resource.

    Table schema is a simple language- and implementation-agnostic way to declare a
    schema for tabular data. Table schema is well suited for use cases around handling
    and validating tabular data in text formats such as CSV, but its utility extends
    well beyond this core usage, towards a range of applications where data benefits
    from a portable schema format.

    Attributes:
        fields (list[FieldProperties]): Specifies the fields in this table schema.
        fields_match (FieldsMatchType): Specifies how fields in the table
            schema match the fields in the data source.
        primary_key (list[str] | str): A primary key is a field name or an array of
            field names, whose values must uniquely identify each row in the table.
        unique_keys (list[list[str]]): A field or a set of fields that are
            required to have unique logical values in each row in the table.
        foreign_keys (list[TableSchemaForeignKeyProperties]): A reference where
            values in a field (or fields) on the table (resource) described by this
            table schema connect to values in a field (or fields) on this or a separate
            table (resource).
        missing_values (list[str] | list[MissingValueProperties]): Values that,
            when encountered in the source, should be considered as not present.
    """

    fields: list[FieldProperties] = field(default_factory=list)
    fields_match: FieldsMatchType = "exact"
    primary_key: list[str] | str = ""
    unique_keys: list[list[str]] = field(default_factory=list)
    foreign_keys: list[TableSchemaForeignKeyProperties] = field(default_factory=list)
    missing_values: list[str] | list[MissingValueProperties] = field(
        default_factory=lambda: [""]
    )


@dataclass
class ResourceProperties(Properties):
    """A data resource.

    A simple format to describe and package a single data resource such as an
    individual table or file. The essence of a data resource is a locator for
    the data it describes. A range of other properties can be declared to provide a
    richer set of metadata.

    Attributes:
        name (str): A simple name or identifier to be used for this resource.
            Should consist only of lowercase English alphanumeric characters plus
            characters in `.-_`.
        path (str): A path pointing to the data for this resource.
        type (Literal['table']): Specifies the type of the resource.
        title (str): A human-readable title.
        description (str): A text description. Markdown is encouraged.
        sources (list[SourceProperties]): The raw sources for this resource.
        licenses (list[LicenseProperties]): The license(s) under which the
            resource is published.
        format (str): The file format of this resource. Expected to be the
            standard file extension.
        mediatype (str): The media type of this resource. Can be any
            valid media type listed with
            [IANA](https://www.iana.org/assignments/media-types/media-types.xhtml).
        encoding (str): The file encoding of this resource.
        bytes (int): The size of this resource in bytes.
        hash (str): The MD5 hash of this resource. Indicate other
            hashing algorithms with the {algorithm}:{hash} format.
        dialect (TableDialectProperties): The tabular dialect of the resource data.
        schema (TableSchemaProperties): A table schema for the resource data,
            compliant with the table schema specification.
    """

    name: str = ""
    path: str = ""
    type: Literal["table"] = "table"
    title: str = ""
    description: str = ""
    sources: list[SourceProperties] = field(default_factory=list)
    licenses: list[LicenseProperties] = field(default_factory=list)
    format: str = ""
    mediatype: str = ""
    encoding: str = "utf-8"
    bytes: int = 0
    hash: str = ""
    dialect: TableDialectProperties = field(default_factory=TableDialectProperties)
    schema: TableSchemaProperties = field(default_factory=TableSchemaProperties)


@dataclass
class PackageProperties(Properties):
    """A data package.

    A simple container format for describing a coherent collection of data in a single
    "package". It provides the basis for convenient delivery, installation and
    management of datasets.

    Attributes:
        name (str): A simple name or identifier to be used for this package.
            Should consist only of lowercase English alphanumeric characters plus
            characters in `.-_`.
        id (str): The unique identifier of this package.
        title (str): A human-readable title.
        description (str): A text description. Markdown is encouraged.
        homepage (str): The home on the web that is related to this package.
        version (str): A version string identifying the version of this package.
        created (str): The datetime on which this package was created.
        contributors (list[ContributorProperties]): The people or organizations
            who contributed to this package.
        keywords (list[str]): A list of keywords that describe this package.
        image (str): An image to represent this package.
        licenses (list[LicenseProperties]): The license(s) under which this
            package is published.
        resources (list[ResourceProperties]): Specifies the data resources
            in this data package, each compliant with the data resource specification.
        sources (list[SourceProperties]): The raw sources for this data package.
    """

    name: str = ""
    id: str = ""
    title: str = ""
    description: str = ""
    homepage: str = ""
    version: str = ""
    created: str = ""
    contributors: list[ContributorProperties] = field(default_factory=list)
    keywords: list[str] = field(default_factory=list)
    image: str = ""
    licenses: list[LicenseProperties] = field(default_factory=list)
    resources: list[ResourceProperties] = field(default_factory=list)
    sources: list[SourceProperties] = field(default_factory=list)
