import polars as pl
from pytest import mark
from xlwt import Workbook

from seedcase_sprout.core.extract_resource_properties import extract_resource_properties

empty_data = pl.DataFrame([])
schema_empty_data = {"fields": []}

tidy_data = pl.DataFrame(
    {
        "id": [1, 2, 3],
        "name": ["Alice", "Bob", "Charlie"],
        "dob": ["2000-09-22", "1996-11-12", "1998-03-15"],
        "height": [1.7, 1.6, 1.8],
        "survey_datetime": [
            "2020-01-02 08:00:00",
            "2021-02-03 09:00:00",
            "2022-03-04 10:00:00",
        ],
        "completed": [True, False, True],
        "survey_year": [2020, 2021, 2022],
        "survey_starttime": ["08:00:00", "09:00:00", "10:00:00"],
        "survey_duration": ["PT1M30S", "PT1H30M", "PT1H"],
        "survey_yearmonth": ["2020-01", "2021-02", "2022-03"],
        "survey_geopoint": ["1.0,2.0", "3.0,4.0", "5.0,6.0"],
        "survey_array": [
            '[{"name":"value1", "details": {"subfield1": "1", "subfield2": "2"}}]',
            '[{"name":"value2", "details": {"subfield1": "5", "subfield2": "6"}}]',
            '[{"name":"value3", "details": {"subfield1": "7", "subfield2": "8"}}]',
        ],
        "survey_geojson": [
            '{"type": "Feature", '
            '"geometry": {"type": "Point", "coordinates": [102.0, 0.5]}, '
            '"properties": {"name": "value1"}}',
            '{"type": "Feature", '
            '"geometry": {"type": "Point", "coordinates": [103.0, 1.0]}, '
            '"properties": {"name": "value1"}}',
            '{"type": "Feature", '
            '"geometry": {"type": "Point", "coordinates": [104.0, 0.0]}, '
            '"properties": {"name": "value1"}}',
        ],
        "object": [
            '{"answer_q1": "No", "answer_q2": "Yes"}',
            '{"answer_q1": "Yes", "answer_q2": "Yes"}',
            '{"answer_q1": "No", "answer_q2": "No"}',
        ],
    }
)
schema_tidy_data = {
    "fields": [
        {"name": "id", "type": "integer"},
        {"name": "name", "type": "string"},
        {"name": "dob", "type": "date"},
        {"name": "height", "type": "number"},
        {"name": "survey_datetime", "type": "datetime"},
        {"name": "completed", "type": "boolean"},
        {
            "name": "survey_year",
            "type": "integer",
        },  # Frictionless detects year as integer
        {"name": "survey_starttime", "type": "time"},
        {"name": "survey_duration", "type": "duration"},
        {"name": "survey_yearmonth", "type": "yearmonth"},
        {"name": "survey_geopoint", "type": "geopoint"},
        {"name": "survey_array", "type": "array"},
        {"name": "survey_geojson", "type": "geojson"},
        {"name": "object", "type": "object"},
    ]
}

non_tidy_data = pl.DataFrame(
    {
        "id": [1, 2, "NA"],
        "name": ["Alice", 10, "Charlie"],
        "dob": ["2000-09-22", "1996-11-12", "1998-03-15 00:00:00"],
        "height": [1.7, 1.6, 1],
        "survey_datetime": [
            "2020-01-02 08:00:00",
            "2021-02-03",
            "2022-03-04 10:00:00",
        ],
        "completed": [True, False, 1],
        "survey_year": [20, 21, 2022],
        "survey_starttime": ["08:00", "09:00:00", "10"],
        "survey_duration": ["1:00", "PT1H30M", "PT1H"],
        "survey_yearmonth": ["2020 01", "02-2021", "2022-03"],
        "survey_geopoint": ["1.0,2.0", "3.0", "5.0,6.0"],
        "survey_array": [
            '[{"name":"value1", "details": {"subfield1": "1", "subfield2": "2"}}]',
            "",
            '[{"name":"value3"}]',
        ],
        "survey_geojson": [
            '{"type": "Feature", '
            '"geometry": {"type": "Point", "coordinates": [102.0, 0.5]}, '
            '{"type": "Feature"}',
            '{"type": "Feature", ',
            '"geometry": {"type": "Point", "coordinates": [104.0, 0.0]}, '
            '"properties": {"name": "value1"}}',
        ],
        "object": ["{}", "", '{"answer_q1": "No"}'],
    },
    strict=False,
)
# With mixed data types, the Frictionless library mostly defaults to string
schema_non_tidy_data = {
    "fields": [
        {"name": "id", "type": "string"},
        {"name": "name", "type": "string"},
        {"name": "dob", "type": "string"},
        {"name": "height", "type": "number"},
        {"name": "survey_datetime", "type": "string"},
        {
            "name": "completed",
            "type": "integer",
        },  # Frictionless detects Boolean as integer when an integer is present
        {"name": "survey_year", "type": "integer"},
        {"name": "survey_starttime", "type": "string"},
        {"name": "survey_duration", "type": "string"},
        {"name": "survey_yearmonth", "type": "string"},
        {"name": "survey_geopoint", "type": "string"},
        {"name": "survey_array", "type": "array"},
        {"name": "survey_geojson", "type": "string"},
        {"name": "object", "type": "object"},
    ]
}


@mark.parametrize(
    "data, expected_schema",
    [
        (empty_data, schema_empty_data),
        (tidy_data, schema_tidy_data),
        (non_tidy_data, schema_non_tidy_data),
    ],
)
def test_returns_expected_resource_properties_from_csv_file(
    tmp_path, data, expected_schema
):
    """Returns expected resource properties from a non-empty csv file."""
    # Given
    file_path = tmp_path / "data.csv"
    data.write_csv(file_path)

    expected_properties_compact_dict = {
        "name": "data",
        "path": str(file_path),
        "type": "table",
        "format": "csv",
        "mediatype": "text/csv",
        "encoding": "utf-8",
        "schema": expected_schema,
    }
    # When
    properties = extract_resource_properties(file_path)

    # Then
    assert properties.compact_dict == expected_properties_compact_dict


@mark.parametrize(
    "data, expected_schema",
    [
        (empty_data, schema_empty_data),
        (tidy_data, schema_tidy_data),
        (non_tidy_data, schema_non_tidy_data),
    ],
)
def test_returns_expected_resource_properties_from_tsv_file(
    tmp_path, data, expected_schema
):
    """Returns expected resource properties from a non-empty tsv file."""
    # Given
    file_path = tmp_path / "data.tsv"
    data.write_csv(file_path, separator="\t")

    expected_properties_compact_dict = {
        "name": "data",
        "path": str(file_path),
        "type": "table",
        "format": "tsv",
        "mediatype": "text/tsv",
        "encoding": "utf-8",
        "schema": expected_schema,
    }
    # When
    properties = extract_resource_properties(file_path)

    # Then
    assert properties.compact_dict == expected_properties_compact_dict


@mark.parametrize("extension", ["parq", "parquet"])
@mark.parametrize(
    "data, expected_schema",
    [
        (empty_data, schema_empty_data),
        (tidy_data, schema_tidy_data),
        (non_tidy_data, schema_non_tidy_data),
    ],
)
def test_returns_expected_resource_properties_from_parquet_file(
    tmp_path, data, expected_schema, extension
):
    """Returns expected resource properties from a non-empty parquet file."""
    # Given
    file_path = tmp_path / f"data.{extension}"
    data.write_parquet(file_path)

    expected_properties_compact_dict = {
        "name": "data",
        "path": str(file_path),
        "type": "table",
        "format": f"{extension}",
        "mediatype": "application/parquet",
        "schema": expected_schema,
    }
    # When
    properties = extract_resource_properties(file_path)

    # Then
    assert properties.compact_dict == expected_properties_compact_dict


@mark.parametrize(
    "data, expected_schema",
    [
        (empty_data, schema_empty_data),
        (tidy_data, schema_tidy_data),
        (non_tidy_data, schema_non_tidy_data),
    ],
)
def test_returns_expected_resource_properties_from_xlsx_file(
    tmp_path, data, expected_schema
):
    """Returns expected resource properties from an xlsx file."""
    # Given
    file_path = tmp_path / "data.xlsx"
    data.write_excel(file_path)

    expected_properties_compact_dict = {
        "name": "data",
        "path": str(file_path),
        "type": "table",
        "format": "xlsx",
        "mediatype": "application/vnd.ms-excel",
        "encoding": "utf-8",
        "schema": expected_schema,
    }
    # When
    properties = extract_resource_properties(file_path)

    # Then
    assert properties.compact_dict == expected_properties_compact_dict


@mark.parametrize(
    "data, expected_schema",
    [
        (empty_data, schema_empty_data),
        (tidy_data, schema_tidy_data),
        (non_tidy_data, schema_non_tidy_data),
    ],
)
def test_returns_expected_resource_properties_from_xls_file(
    tmp_path, data, expected_schema
):
    """Returns expected resource properties from an xls file."""
    # Given
    file_path = tmp_path / "data.xls"

    wb = Workbook()
    ws = wb.add_sheet("sheet1")
    for i, header in enumerate(data.columns):
        ws.write(0, i, header)
    for i, row in enumerate(data.rows()):
        for j, cell in enumerate(row):
            ws.write(i + 1, j, cell)
    wb.save(tmp_path / "data.xls")

    expected_properties_compact_dict = {
        "name": "data",
        "path": str(file_path),
        "type": "table",
        "format": "xls",
        "mediatype": "application/vnd.ms-excel",
        "encoding": "utf-8",
        "schema": expected_schema,
    }
    # When
    properties = extract_resource_properties(file_path)

    # Then
    assert properties.compact_dict == expected_properties_compact_dict


@mark.parametrize(
    "data, expected_schema",
    [  # No empty data since that isn't valid json
        (tidy_data, schema_tidy_data),
        (non_tidy_data, schema_non_tidy_data),
    ],
)
def test_returns_expected_resource_properties_from_json_file(
    tmp_path, data, expected_schema
):
    """Returns expected resource properties from json files."""
    # Given
    file_path = tmp_path / "data.json"
    data.write_json(file_path)

    expected_properties_compact_dict = {
        "name": "data",
        "path": str(file_path),
        "type": "table",
        "format": "json",
        "mediatype": "text/json",
        "encoding": "utf-8",
        "schema": expected_schema,
    }
    # When
    properties = extract_resource_properties(file_path)

    # Then
    assert properties.compact_dict == expected_properties_compact_dict


@mark.parametrize("extension", {"jsonl", "ndjson"})
@mark.parametrize(
    "data, expected_schema",
    [  # No empty data since that isn't valid jsonl/ndjson
        (tidy_data, schema_tidy_data),
        (non_tidy_data, schema_non_tidy_data),
    ],
)
def test_returns_expected_resource_properties_from_newline_delimited_json_file(
    tmp_path, extension, data, expected_schema
):
    """Returns expected resource properties from a newline delimited json files."""
    # Given
    file_path = tmp_path / f"data.{extension}"
    data.write_ndjson(file_path)

    expected_properties_compact_dict = {
        "name": "data",
        "path": str(file_path),
        "type": "table",
        "format": f"{extension}",
        "mediatype": f"text/{extension}",
        "encoding": "utf-8",
        "schema": expected_schema,
    }
    # When
    properties = extract_resource_properties(file_path)

    # Then
    assert properties.compact_dict == expected_properties_compact_dict
