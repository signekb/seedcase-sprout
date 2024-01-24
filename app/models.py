from django.db import models
from django.conf import settings


class TableMetadata(models.Model):
    name = models.CharField(max_length=128)
    original_file_name = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, default=None, # remove default=None, when we start handling users
                                   on_delete=models.PROTECT, related_name='creator')
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True,
                                    on_delete=models.PROTECT, related_name='modifier')


class ColumnDataType(models.Model):
    display_name = models.TextField()
    description = models.TextField()


class ColumnMetadata(models.Model):
    table_metadata = models.ForeignKey(TableMetadata, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    description = models.TextField()
    data_type = models.ForeignKey(ColumnDataType, on_delete=models.PROTECT)
    allow_missing_value = models.BooleanField()
    allow_duplicate_value = models.BooleanField()
