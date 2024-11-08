"""File containing database utility functions used for testing."""

from seedcase_sprout.app.models import Columns, Tables


def create_table(name: str) -> Tables:
    """Creates Tables based on a name.

    Args:
        name: Name of the table

    Returns:
        Tables: A instance of Tables representing a data set
    """
    return Tables(
        name=name,
        original_file_name=name + ".csv",
        description=name + " description",
    )


def create_column(name: str, table: Tables) -> Columns:
    """Creates Columns based on a column name and a table.

    Args:
        name: The name of the column
        table: The table the column belongs to

    Returns:
        Columns: The column created
    """
    return Columns(
        tables=table,
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
    """Creates Tables and Columns based on table name and column name.

    Args:
        table_name: The table name for Tables
        column_name: The column name for Columns
    """
    table = create_table(table_name)
    table.save()

    column = create_column(column_name, table)
    column.save()
