# NOTE: This content is modified from the auto-generated
# `generate_properties/generated_properties.py` file. Update the auto-generated
# properties file to add more dataclasses and move them into this file.


from dataclasses import dataclass, field
from typing import Any, Literal


@dataclass
class ContributorProperties:
    """A contributor to this descriptor.

    Attributes:
        - title (str | None): A human-readable title.
        - path (str | None): A fully qualified URL, or a POSIX file path.
        - email (str | None): An email address.
        - given_name (str | None):
        - family_name (str | None):
        - organization (str | None): An organizational affiliation for this
        contributor.
        - roles (list[str] | None):
    """

    title: str | None = None
    path: str | None = None
    email: str | None = None
    given_name: str | None = None
    family_name: str | None = None
    organization: str | None = None
    roles: list[str] | None = None


@dataclass
class LicenseProperties:
    """A license for this descriptor.

    Attributes:
        - name (str | None): MUST be an Open Definition license identifier,
        see http://licenses.opendefinition.org/
        - path (str | None): A fully qualified URL, or a POSIX file path.
        - title (str | None): A human-readable title.
    """

    name: str | None = None
    path: str | None = None
    title: str | None = None


@dataclass
class SourceProperties:
    """A source file.

    Attributes:
        - title (str | None): A human-readable title.
        - path (str | None): A fully qualified URL, or a POSIX file path.
        - email (str | None): An email address.
        - version (str | None):
    """

    title: str | None = None
    path: str | None = None
    email: str | None = None
    version: str | None = None


@dataclass
class TableDialectProperties:
    r"""The Table dialect descriptor.

    Attributes:
        - header (bool | None): Specifies if the file includes a header row,
        always as the first row in the file.
        - header_rows (list[int] | None):
        - header_join (str | None):
        - comment_rows (list[int] | None):
        - comment_char (str | None): Specifies that any row beginning with
        this one-character string, without preceeding whitespace, causes the
        entire line to be ignored.
        - delimiter (str | None): A character sequence to use as the field
        separator.
        - line_terminator (str | None): Specifies the character sequence that
        must be used to terminate rows.
        - quote_char (str | None): Specifies a one-character string to use as
        the quoting character.
        - double_quote (bool | None): Specifies the handling of quotes inside
        fields.
        - escape_char (str | None): Specifies a one-character string to use as
        the escape character.
        - null_sequence (str | None): Specifies the null sequence, for
        example, `\\N`.
        - skip_initial_space (bool | None): Specifies the interpretation of
        whitespace immediately following a delimiter. If false, whitespace
        immediately after a delimiter should be treated as part of the
        subsequent field.
        - property (str | None):
        - item_type (Literal['array', 'object'] | None):
        - item_keys (list[str] | None):
        - sheet_number (int | None):
        - sheet_name (str | None):
        - table (str | None):
    """

    header: bool | None = True
    header_rows: list[int] | None = field(default_factory=lambda: [1])
    header_join: str | None = " "
    comment_rows: list[int] | None = field(default_factory=lambda: [1])
    comment_char: str | None = None
    delimiter: str | None = ","
    line_terminator: str | None = "\r\n"
    quote_char: str | None = '"'
    double_quote: bool | None = True
    escape_char: str | None = None
    null_sequence: str | None = None
    skip_initial_space: bool | None = False
    property: str | None = None
    item_type: Literal["array", "object"] | None = None
    item_keys: list[str] | None = None
    sheet_number: int | None = None
    sheet_name: str | None = None
    table: str | None = None


@dataclass
class ReferenceProperties:
    """Reference for a foreign key.

    Attributes:
        - resource: (str | None): The resource pointed to by the foreign key.
        - fields: (list[str] | None): The fields pointed to by the foreign key.
    """

    resource: str | None = None
    fields: list[str] | None = None


@dataclass
class TableSchemaForeignKeyProperties:
    """Table Schema Foreign Key.

    Attributes:
        - fields (list[str] | None):
        - reference (ReferenceProperties | None):
    """

    fields: list[str] | None = None
    reference: ReferenceProperties | None = None


@dataclass
class MissingValueProperties:
    """Values that when encountered in the source, should be considered as not present.

    Attributes:
        - value (str | None):
        - label (str | None):
    """

    value: str | None = None
    label: str | None = None


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
class ConstraintsProperties:
    """A class used by consumers to list constraints for validating field values.

    Attributes:
        - required (bool | None): Indicates whether a property must have a
        value for each instance.
        - unique (bool | None): When `true`, each value for the property
        `MUST` be unique.
        - pattern (str | None): A regular expression pattern to test each
        value of the property against, where a truthy response indicates
        validity.
        - enum (list | None): The value of the field must exactly match one of
        the values in the enum array.
        - min_length (int | None): An integer that specifies the minimum
        length of a value.
        - max_length (int | None): An integer that specifies the maximum
        length of a value.
        - minimum (str | float | int | None): Specifies a minimum value for a field.
        - maximum (str | float | int | None): Specifies a maximum value for a field.
        - exclusive_minimum (str | float | int | None): Specifies an exclusive minimum
        value for a field.
        - exclusive_maximum (str | float | int | None): Specifies an exclusive maximum
        value for a field.
        - json_schema (dict[str, Any] | None): A valid JSON Schema object to
        validate field values. If a field value conforms to the provided
        JSON Schema then this field value is valid.
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
class FieldProperties:
    """A field in a Table Schema.

    Attributes:
        - name (str | None): A name for this field. Must be unique amongst other field
        names in this Table Schema.
        - title (str | None): A human readable label or title for this field.
        - type (FieldType | None): The data type of this field.
        - format (str | None): The format for this field.
        - description (str | None): A text description for this field.
        - example (str | None): An example value for this field.
        - constraints (ConstraintsProperties | None): The constraints applicable to
        this field.
        - categories (list[str] | list[int] | None): A finite set of possible values
        for this field.
        - categories_ordered (bool | None): Specifies whether the order of appearance
        of the values in the `categories` property should be regarded as their natural
        order.
        - missing_values (list[str] | list[MissingValueProperties] | None): Values that
        when encountered in the source, should be considered as not present. Takes
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


# Allowed strategies for matching fields in the Table Schema to fields the data source.
FieldsMatchType = Literal["exact", "equal", "subset", "superset", "partial"]


@dataclass
class TableSchemaProperties:
    """A Table Schema for this resource, compliant with the Table Schema specification.

    Attributes:
        - fields (list[FieldProperties] | None): An `array` of Table Schema Field
        objects.
        - fields_match (FieldsMatchType | None):
        - primary_key (list[str] | str | None): A primary key is a field name
        or an array of field names, whose values `MUST` uniquely identify
        each row in the table.
        - unique_keys (list[list[str]] | None):
        - foreign_keys (list[TableSchemaForeignKeyProperties] | None):
        - missing_values (list[str] | list[MissingValueProperties] | None): Values that
        when encountered in the source, should be considered as `null`, 'not
        present', or 'blank' values.
    """

    fields: list[FieldProperties] | None = None
    fields_match: FieldsMatchType | None = "exact"
    primary_key: list[str] | str | None = None
    unique_keys: list[list[str]] | None = None
    foreign_keys: list[TableSchemaForeignKeyProperties] | None = None
    missing_values: list[str] | list[MissingValueProperties] | None = field(
        default_factory=lambda: [""]
    )


@dataclass
class ResourceProperties:
    """Data Resource.

    Attributes:
        - name (str | None): An identifier string.
        - id (str | None): The unique identifier of this resource.
        - path (str | None): A path pointing to the data for this resource.
        - data (Any | None): Inline data for this resource.
        - type (Literal['table'] | None):
        - title (str | None): A human-readable title.
        - description (str | None): A text description. Markdown is
        encouraged.
        data package.
        - sources (list[SourceProperties] | None): The raw sources for this resource.
        - licenses (list[LicenseProperties] | None): The license(s) under which the
        resource is published.
        - format (str | None): The file format of this resource.
        - mediatype (str | None): The media type of this resource. Can be any
        valid media type listed with
        [IANA](https://www.iana.org/assignments/media-types/media-
        types.xhtml).
        - encoding (str | None): The file encoding of this resource.
        - bytes (int | None): The size of this resource in bytes.
        - hash (str | None): The MD5 hash of this resource. Indicate other
        hashing algorithms with the {algorithm}:{hash} format.
        - dialect (TableDialectProperties | None): The Table dialect descriptor.
        - schema (TableSchemaProperties | None): A Table Schema for this resource,
        compliant with the [Table Schema](/tableschema/) specification.
    """

    name: str | None = None
    id: str | None = None
    path: str | None = None
    data: Any | None = None
    type: Literal["table"] | None = None
    title: str | None = None
    description: str | None = None
    sources: list[SourceProperties] | None = None
    licenses: list[LicenseProperties] | None = None
    format: str | None = None
    mediatype: str | None = None
    encoding: str | None = "utf-8"
    bytes: int | None = None
    hash: str | None = None
    dialect: TableDialectProperties | None = None
    schema: TableSchemaProperties | None = None


@dataclass
class PackageProperties:
    """Data Package.

    Attributes:
        - name (str | None): An identifier string.
        - id (str | None): A property reserved for globally unique
        identifiers. Examples of identifiers that are unique include UUIDs
        and DOIs.
        - title (str | None): A human-readable title.
        - description (str | None): A text description. Markdown is
        encouraged.
        - homepage (str | None): The home on the web that is related to this
        data package.
        - version (str | None): A unique version number for this descriptor.
        - created (str | None): The datetime on which this descriptor was
        created.
        - contributors (list[ContributorProperties] | None): The contributors to this
        descriptor.
        - keywords (list[str] | None): A list of keywords that describe this
        package.
        - image (str | None): A image to represent this package.
        - licenses (list[LicenseProperties] | None): The license(s) under which this
        package is published.
        - resources (list[ResourceProperties] | None): An `array` of Data Resource
        objects, each compliant with the [Data Resource](/data-resource/)
        specification.
        - sources (list[SourceProperties] | None): The raw sources for this resource.
    """

    name: str | None = None
    id: str | None = None
    title: str | None = None
    description: str | None = None
    homepage: str | None = None
    version: str | None = None
    created: str | None = None
    contributors: list[ContributorProperties] | None = None
    keywords: list[str] | None = None
    image: str | None = None
    licenses: list[LicenseProperties] | None = None
    resources: list[ResourceProperties] | None = None
    sources: list[SourceProperties] | None = None
