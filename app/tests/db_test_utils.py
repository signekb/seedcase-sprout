"""File contains some database utility functions used for testing."""
from app.models import ColumnMetadata, TableMetadata


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


def create_column(name: str, table: TableMetadata) -> ColumnMetadata:
    """Creates ColumnMetadata based on a column name.

    Args:
        name: The name of the column
        table: The table where the column belongs

    Returns:
        ColumnMetaData: The column created
    """
    return ColumnMetadata(
        table_metadata=table,
        name=name,
        title=name + "Title",
        description=name + " description",
        data_type_id=1,
        allow_missing_value=True,
        allow_duplicate_value=True,
    )


def create_metadata_table_and_column(
    table_name: str = "TestTable", column_name: str = "Column"
) -> None:
    """Create a MetaDataTable and a MetaDataColumn.

    Args:
        table_name: The table name for MetaDataTable
        column_name: The column name for MetaDataColumn
    """
    table = create_table(table_name)
    table.save()

    column = create_column(column_name, table)
    column.save()
