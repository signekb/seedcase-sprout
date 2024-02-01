from app.models import TableMetadata, ColumnMetadata


def create_table(name: str):
    return TableMetadata(
        name=name, original_file_name=name + ".csv", description=name + " description"
    )


def create_column(name: str, table: TableMetadata):
    return ColumnMetadata(
        table_metadata=table,
        name=name,
        title=name + "Title",
        description=name + " description",
        data_type_id=1,
        allow_missing_value=True,
        allow_duplicate_value=True,
    )


def create_metadata_table_and_column(table_name: str = "TestTable",
                                     column_name: str = "Column"):
    table = create_table(table_name)
    table.save()

    column = create_column(column_name, table)
    column.save()
