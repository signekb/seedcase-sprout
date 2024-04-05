"""File containing database utility functions used for testing."""

from sprout.models import Columns, TableMetadata


def create_table(name: str) -> TableMetadata:
    """Creates TableMetaData based on a name.

    Args:
        name: Name of the table

    Returns:
        TableMetadata: A instance of TableMetadata representing a data set
    """
    return TableMetadata(
        name=name,
        original_file_name=name + ".csv",
        description=name + " description",
    )


def create_column(name: str, table: TableMetadata) -> Columns:
    """Creates Columns based on a column name and a table.

    Args:
        name: The name of the column
        table: The table the column belongs to

    Returns:
        Columns: The column created
    """
    return Columns(
        table_metadata=table,
        machine_readable_name=name,
        display_name=name + "display name",
        description=name + " description",
        data_type_id=1,
        allow_missing_value=True,
        allow_duplicate_value=True,
    )


def create_metadata_table_and_column(
    table_name: str = "TestTable", column_name: str = "Column"
) -> None:
    """Creates TableMetadata and Columns based on table name and column name.

    Args:
        table_name: The table name for TableMetadata
        column_name: The column name for Columns
    """
    table = create_table(table_name)
    table.save()

    column = create_column(column_name, table)
    column.save()
