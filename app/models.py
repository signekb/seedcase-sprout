from django.db import models


class TableMetadata(models.Model):
    name = models.CharField(max_length=128)
    original_file_name = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.IntegerField()


class ColumnDataType(models.Model):
    display_name = models.TextField()


class ColumnMetadata(models.Model):
    table_metadata = models.ForeignKey(TableMetadata, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    description = models.TextField()
    data_type = models.ForeignKey(ColumnDataType, on_delete=models.PROTECT)
    allow_missing_value = models.BooleanField()
    allow_duplicate_value = models.BooleanField()
