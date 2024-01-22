from app.models import TableMetadata, ColumnMetadata


def create_table(name):
    return TableMetadata(
        name=name, original_file_name=name + ".csv", description=name + " description"
    )


def create_column(name, table):
    return ColumnMetadata(
        table_metadata=table,
        name=name,
        title=name + "Title",
        description=name + " description",
        data_type_id=1,
        allow_missing_value=True,
        allow_duplicate_value=True,
    )


def create_metadata_table_and_column():
    table = create_table("TestTable")
    table.save()

    column = create_column("Column", table)
    column.save()
